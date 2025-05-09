import os
from datetime import datetime, timedelta
from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    status,
    Form,
    WebSocket,
    WebSocketDisconnect,
    Query,
    Request,
)
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import FileResponse, RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from jose import JWTError, jwt
from passlib.context import CryptContext
import logging
import uvicorn
import json
from cache import redis_client
from mongodb import (
    users_collection,
    chats_collection,
    messages_collection,
    user_chats_collection,
)
from models_mongo import UserModel, ChatModel, MessageModel, UserChatsModel

LOG = logging.getLogger("uvicorn.error")
LOG.info("API is starting up")
LOG.info(uvicorn.Config.asgi_version)
from uuid import UUID

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# OAuth2 and JWT settings
SECRET_KEY = "your-secret-key"  # replace with a secure secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# Set up the templates directory (ensure you have a folder named "templates")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


async def create_indexes():
    await users_collection.create_index("username", unique=True)
    await messages_collection.create_index([("chat_id", 1), ("sent_datetime", 1)])
    await user_chats_collection.create_index("user_id")


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    # Create MongoDB indexes on startup
    await create_indexes()


from kafka import KafkaProducer
import json

# Initialize a KafkaProducer (adjust bootstrap_servers accordingly)
from kafka import KafkaProducer
import time


def create_kafka_producer():
    for _ in range(5):  # Retry up to 5 times
        try:
            producer = KafkaProducer(
                bootstrap_servers=["localhost:9092"],  # kafka vs localhost
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            )
            return producer
        except Exception as e:
            LOG.error(f"Kafka connection failed: {e}. Retrying in 5 seconds...")
            time.sleep(5)
    raise Exception("Failed to connect to Kafka after 5 retries")


producer = create_kafka_producer()


# producer = KafkaProducer(
#     bootstrap_servers=["localhost:9092"],
#     value_serializer=lambda v: json.dumps(v).encode("utf-8"),
# )


# Helpers for password verification and token creation
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now() + (
        expires_delta if expires_delta else timedelta(minutes=15)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Instead of a DB dependency, we use Motor functions directly
async def get_user(username: str):
    user = await users_collection.find_one({"username": username})
    return user


def get_token_from_request(request: Request):
    token = request.cookies.get("access_token")
    if token:
        return token
    auth_header: str = request.headers.get("Authorization")
    if auth_header:
        scheme, _, token = auth_header.partition(" ")
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=401, detail="Invalid authentication scheme."
            )
        return token
    raise HTTPException(status_code=401, detail="Not authenticated.")


# Endpoint to obtain a token using username and password
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user(form_data.username)
    if not user or not verify_password(form_data.password, user.get("password")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.get("username"), "id": str(user.get("id"))},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


# Serve the welcome page
@app.get("/")
async def welcome():
    return FileResponse(os.path.join(BASE_DIR, "templates/welcome.html"))


# Serve the login page
@app.get("/login")
async def login_page():
    return FileResponse(os.path.join(BASE_DIR, "templates/login.html"))


# Serve the signup page
@app.get("/signup")
async def signup_page():
    return FileResponse(os.path.join(BASE_DIR, "templates/signup.html"))


# Process signup form submissions
@app.post("/signup")
async def process_signup(
    username: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
):
    if password != confirm_password:
        return RedirectResponse(
            url="/signup?error=Passwords+do+not+match", status_code=303
        )
    existing_user = await users_collection.find_one({"username": username})
    if existing_user:
        return RedirectResponse(
            url="/signup?error=Username+already+taken", status_code=303
        )
    hashed_password = get_password_hash(password)
    user = UserModel(
        username=username, password=hashed_password
    )  ### user already exist ?
    await users_collection.insert_one(user.dict())
    # LOG.info(f"User {user.dict()} created successfully.")
    return RedirectResponse(url="/login", status_code=303)


@app.post("/chats/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie(key="access_token")
    return response


@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user(form_data.username)
    if not user or not verify_password(form_data.password, user.get("password")):
        return RedirectResponse(url="/login?error=Invalid+credentials", status_code=303)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.get("username"), "id": str(user.get("id"))},
        expires_delta=access_token_expires,
    )
    # LOG.info(f"User {user.get('username')} logged in successfully.")
    response = RedirectResponse(url="/chats", status_code=303)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response


@app.get("/chats")
async def chats_page(request: Request):
    token = get_token_from_request(request)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Query user_chats collection for this user’s chats
    cursor = user_chats_collection.find({"user_id": UUID(user_id)})
    user_chats = await cursor.to_list(length=100)
    chat_ids = [user_chat.get("chat_id") for user_chat in user_chats]

    chat_data = []
    for chat_id in chat_ids:
        # Retrieve the chat document
        chat = await chats_collection.find_one({"id": chat_id})
        if not chat:
            continue
        # Get the last message (sorted descending by sent_datetime)
        last_message = await messages_collection.find_one(
            {"chat_id": chat_id}, sort=[("sent_datetime", -1)]
        )
        # Determine other participant(s) username(s)
        other_usernames = []
        for participant in chat.get("participants", []):
            if str(participant) != str(user_id):
                user_doc = await users_collection.find_one({"id": participant})
                if user_doc and user_doc.get("username"):
                    other_usernames.append(user_doc.get("username"))
        name = ", ".join(other_usernames) if other_usernames else "Unknown"

        chat_data.append(
            {
                "id": str(chat.get("id")),
                "name": name,
                "last_message": last_message,  # Expect last_message to be a dict (or None)
                "last_message_time": chat.get("last_message_datetime"),
            }
        )

        # Sort chats by last_message_time in descending order
        chat_data.sort(key=lambda x: x["last_message_time"], reverse=True)

    return templates.TemplateResponse(
        "chats.html", {"request": request, "chats": chat_data}
    )


@app.post("/chats/create")
async def create_chat(
    request: Request,
    recipient_username: str = Form(...),
):
    token = get_token_from_request(request)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        creator_id = payload.get("id")
        if creator_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Check if recipient exists
    recipient = await users_collection.find_one({"username": recipient_username})
    if not recipient:
        return RedirectResponse(url="/chats?error=Recipient+not+found", status_code=303)
    recipient_id = str(recipient.get("id"))
    # LOG.info(f"Recipient ID: {recipient}")
    # Check if chat already exists
    existing_chat = await chats_collection.find_one(
        {"participants": {"$all": [creator_id, recipient_id]}}
    )
    if existing_chat:
        return RedirectResponse(url=f"/chat/{existing_chat.get('id')}", status_code=303)
    # Create a new chat
    chat_name = f"Chat with {recipient_username}"
    participants = [creator_id, recipient_id]
    # Check if the chat already exists
    existing_chat = await chats_collection.find_one(
        {"participants": {"$all": participants}}
    )
    if existing_chat:
        return RedirectResponse(url=f"/chat/{existing_chat.get('id')}", status_code=303)
    # If not, create a new chat
    # Create a new chat document
    chat = ChatModel(
        last_message_datetime=datetime.now(),
        participants=participants,
    )
    result = await chats_collection.insert_one(chat.dict())

    chat_id = str(result.inserted_id)

    # Add chat entries for each participant
    for participant in participants:
        user_chat = UserChatsModel(
            user_id=participant,
            chat_id=chat.id,
            last_message_datetime=chat.last_message_datetime,
        )
        await user_chats_collection.insert_one(user_chat.dict())

    return RedirectResponse(url=f"/chat/{chat.id}", status_code=303)


@app.get("/chat/{chat_id}", response_class=HTMLResponse)
async def chat_page(chat_id: str, request: Request):
    token = get_token_from_request(request)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Verify that the chat exists and the user is a participant.
    chat = await chats_collection.find_one({"id": UUID(chat_id)})
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    participants = chat.get("participants", [])
    if str(user_id) not in [str(p) for p in participants]:
        raise HTTPException(status_code=403, detail="Access denied to this chat")

    # Retrieve messages sorted by sent_datetime.
    cursor = messages_collection.find({"chat_id": UUID(chat_id)}).sort(
        "sent_datetime", 1
    )
    messages = await cursor.to_list(length=100)

    # Enrich each message with sender details.
    for msg in messages:
        # Look up the sender document based on sender_id.
        sender = await users_collection.find_one({"id": msg["sender_id"]})
        if sender:
            # Assume sender document has a "username" field.
            msg["sender"] = sender
        else:
            msg["sender"] = {"username": "Unknown"}

    # Determine the other user's name (for a 2-person chat).
    other_user_name = "Unknown"
    for p in participants:
        if str(p) != str(user_id):
            other_user = await users_collection.find_one({"id": p})
            if other_user:
                other_user_name = other_user.get("username", "Unknown")
            break

    return templates.TemplateResponse(
        "chat.html",
        {
            "request": request,
            "chat_id": chat_id,
            "other_user_name": other_user_name,
            "messages": messages,
            "token": token,
        },
    )


@app.post("/chat/{chat_id}/message")
async def post_message(chat_id: str, message: str = Form(...), request: Request = None):
    token = get_token_from_request(request)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Verify that the user participates in the chat
    chat = await chats_collection.find_one({"id": UUID(chat_id)})
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    participants = chat.get("participants", [])
    if str(user_id) not in [str(p) for p in participants]:
        raise HTTPException(status_code=403, detail="Access denied to this chat")

    # # Invalidate the Redis cache for this chat’s messages if applicable
    await redis_client.delete(f"chat:{chat_id}:messages")

    # Prepare the message data.
    message_data = {
        "chat_id": chat_id,
        "sender_id": user_id,
        "sent_datetime": datetime.now().isoformat(),
        "text": message,
    }

    # Publish the message data to a Kafka topic (e.g. "chat_messages")
    producer.send("chat_messages", message_data)
    producer.flush()  # Ensure the message is sent

    return RedirectResponse(url=f"/chat/{chat_id}", status_code=303)


@app.post("/API/signin")
async def api_signin(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user(form_data.username)
    if not user or not verify_password(form_data.password, user.get("password")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.get("username"), "id": str(user.get("id"))},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


from bson import ObjectId


def serialize_mongo_document(document):
    """Convert MongoDB document ObjectId fields to strings."""
    if not document:
        return document
    for key, value in document.items():
        if isinstance(value, ObjectId):
            document[key] = str(value)
    return document


@app.post("/API/signup")
async def api_signup(
    username: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
):
    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    existing_user = await users_collection.find_one({"username": username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    hashed_password = get_password_hash(password)
    user = UserModel(username=username, password=hashed_password)
    await users_collection.insert_one(user.dict())
    return {"message": "User created successfully"}


@app.get("/API/chats")
async def api_get_chats(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    cursor = user_chats_collection.find({"user_id": UUID(user_id)})
    user_chats = await cursor.to_list(length=100)
    chat_ids = [user_chat.get("chat_id") for user_chat in user_chats]

    chat_data = []
    for chat_id in chat_ids:
        chat = await chats_collection.find_one({"id": chat_id})
        if not chat:
            continue
        last_message = await messages_collection.find_one(
            {"chat_id": chat_id}, sort=[("sent_datetime", -1)]
        )
        other_usernames = []
        for participant in chat.get("participants", []):
            if str(participant) != str(user_id):
                user_doc = await users_collection.find_one({"id": participant})
                if user_doc and user_doc.get("username"):
                    other_usernames.append(user_doc.get("username"))
        name = ", ".join(other_usernames) if other_usernames else "Unknown"

        chat_data.append(
            {
                "id": str(chat.get("id")),
                "name": name,
                "last_message": serialize_mongo_document(last_message),
                "last_message_time": chat.get("last_message_datetime"),
            }
        )

    chat_data.sort(key=lambda x: x["last_message_time"], reverse=True)
    return {"chats": chat_data}


@app.post("/API/chats/create")
async def api_create_chat(
    recipient_username: str = Form(...), token: str = Depends(oauth2_scheme)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        creator_id = payload.get("id")
        if creator_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    recipient = await users_collection.find_one({"username": recipient_username})
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")
    recipient_id = str(recipient.get("id"))

    existing_chat = await chats_collection.find_one(
        {"participants": {"$all": [creator_id, recipient_id]}}
    )
    if existing_chat:
        return {"chat_id": str(existing_chat.get("id"))}

    chat = ChatModel(
        last_message_datetime=datetime.now(),
        participants=[creator_id, recipient_id],
    )
    result = await chats_collection.insert_one(chat.dict())
    chat_id = str(result.inserted_id)

    for participant in [creator_id, recipient_id]:
        user_chat = UserChatsModel(
            user_id=participant,
            chat_id=chat.id,
            last_message_datetime=chat.last_message_datetime,
        )
        await user_chats_collection.insert_one(user_chat.dict())

    return {"chat_id": chat.id}


@app.get("/API/chat/{chat_id}")
async def api_get_chat_messages(chat_id: str, token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    chat = await chats_collection.find_one({"id": UUID(chat_id)})
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    participants = chat.get("participants", [])
    if str(user_id) not in [str(p) for p in participants]:
        raise HTTPException(status_code=403, detail="Access denied to this chat")

    cursor = messages_collection.find({"chat_id": UUID(chat_id)}).sort(
        "sent_datetime", 1
    )
    messages = await cursor.to_list(length=100)
    messages = [serialize_mongo_document(msg) for msg in messages]
    return {"messages": messages}


@app.post("/API/chat/{chat_id}/message")
async def api_post_message(
    chat_id: str, message: str = Form(...), token: str = Depends(oauth2_scheme)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    chat = await chats_collection.find_one({"id": UUID(chat_id)})
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    participants = chat.get("participants", [])
    if str(user_id) not in [str(p) for p in participants]:
        raise HTTPException(status_code=403, detail="Access denied to this chat")

    message_data = {
        "chat_id": chat_id,
        "sender_id": user_id,
        "sent_datetime": datetime.now().isoformat(),
        "text": message,
    }
    producer.send("chat_messages", message_data)
    producer.flush()
    return {"message": "Message sent successfully"}
