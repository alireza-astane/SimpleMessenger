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
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from jose import JWTError, jwt  # pip install python-jose[cryptography]
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
    response = RedirectResponse(url="/chats", status_code=303)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response


# Chats page using MongoDB (example: list chats for a user)
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
    # Query user_chats collection to get chats for this user
    cursor = user_chats_collection.find({"user_id": user_id})
    user_chats = await cursor.to_list(length=100)
    # For each chat, you might want to retrieve additional chat details as needed. #TODO
    return templates.TemplateResponse(
        "chats.html", {"request": request, "chats": user_chats}
    )


# Example: serve an individual chat page (this uses SQLAlchemy in your old version;
# here you would query MongoDB for chat details and messages)
@app.get("/chat/{chat_id}")
async def chat_page(chat_id: str, request: Request):
    token = get_token_from_request(request)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    # Retrieve chat details and messages from MongoDB
    chat = await chats_collection.find_one({"id": chat_id})
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    # Fetch messages for the chat
    cursor = messages_collection.find({"chat_id": chat_id}).sort("sent_datetime", 1)
    messages = await cursor.to_list(length=100)
    # Determine other participant's name (requires additional query if needed)
    other_user_name = "Unknown"  # update this as required
    return templates.TemplateResponse(
        "chat.html",
        {
            "request": request,
            "chat_id": chat_id,
            "other_user_name": other_user_name,
            "messages": messages,
        },
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
    LOG.error("here 4")

    # Check if recipient exists
    recipient = await users_collection.find_one({"username": recipient_username})
    if not recipient:
        return RedirectResponse(url="/chats?error=Recipient+not+found", status_code=303)
    recipient_id = str(recipient.get("id"))
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
        user_chat = UserChatsModel(user_id=participant, chat_id=chat_id)
        await user_chats_collection.insert_one(user_chat.dict())

    return RedirectResponse(url=f"/chat/{chat_id}", status_code=303)


# Websocket endpoint remains largely similar (if you still plan to use SQL-based logic for websockets,
# you might also update this to store messages in MongoDB)
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, chat_id: str, websocket: WebSocket):
        await websocket.accept()
        if chat_id not in self.active_connections:
            self.active_connections[chat_id] = []
        self.active_connections[chat_id].append(websocket)

    def disconnect(self, chat_id: str, websocket: WebSocket):
        if chat_id in self.active_connections:
            self.active_connections[chat_id].remove(websocket)

    async def broadcast(self, chat_id: str, message: str):
        if chat_id in self.active_connections:
            for connection in self.active_connections[chat_id]:
                await connection.send_text(message)


manager = ConnectionManager()


@app.websocket("/ws/chat/{chat_id}")
async def chat_websocket(websocket: WebSocket, chat_id: str, token: str = Query(...)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        active_user_id = payload.get("id")
        if active_user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    # (Additional MongoDB-based permission checks may be needed here)
    await manager.connect(chat_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Store the message in MongoDB
            message = MessageModel(
                chat_id=chat_id,
                sender_id=active_user_id,
                sent_datetime=datetime.now(),
                text=data,
            )
            await messages_collection.insert_one(message.dict())
            # Delete Redis cache if used
            await redis_client.delete(f"chat:{chat_id}:messages")
            # Broadcast to connected clients
            await manager.broadcast(chat_id, data)
    except WebSocketDisconnect:
        manager.disconnect(chat_id, websocket)
