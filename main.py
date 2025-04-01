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
from models_mongo import (
    UserModel,
    ChatModel,
    MessageModel,
    UserChatsModel,
)
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from jose import JWTError, jwt  # pip install python-jose[cryptography]
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import Base, User, Chat, Message
import logging
import uvicorn
import json
from cache import redis_client
from mongodb import users_collection, messages_collection, user_chats_collection
from fastapi import FastAPI, Request
from mongodb import (
    users_collection,
    chats_collection,
    messages_collection,
    user_chats_collection,
)
from models_mongo import UserModel, ChatModel, MessageModel  # Your Pydantic models


LOG = logging.getLogger("uvicorn.error")
LOG.info("API is starting up")
LOG.info(uvicorn.Config.asgi_version)

# Create all tables
Base.metadata.create_all(bind=engine)


async def create_indexes():
    await users_collection.create_index("username", unique=True)
    await messages_collection.create_index([("chat_id", 1), ("sent_datetime", 1)])
    await user_chats_collection.create_index("user_id")


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    # Create MongoDB indexes on startup
    await create_indexes()


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# OAuth2 and JWT settings
SECRET_KEY = "your-secret-key"  # replace with a secure secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# Set up the templates directory (ensure you have a folder named "templates")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_token(request: Request):
    # Try to get token from cookie first
    token = request.cookies.get("access_token")
    if token:
        return token
    # Fallback: try to get token from Authorization header
    auth_header: str = request.headers.get("Authorization")
    if auth_header:
        scheme, _, token = auth_header.partition(" ")
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=401, detail="Invalid authentication scheme."
            )
        return token
    raise HTTPException(status_code=401, detail="Not authenticated.")


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now() + (
        expires_delta if expires_delta else timedelta(minutes=15)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Endpoint to obtain a token using username and password
@app.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "id": user.id}, expires_delta=access_token_expires
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


# Process signup form submissions if needed
@app.post("/signup")
async def process_signup(
    username: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db),
):
    if password != confirm_password:
        # In a real app you would want to notify the user of the error.
        return RedirectResponse(
            url="/signup?error=Passwords+do+not+match", status_code=303
        )
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        return RedirectResponse(
            url="/signup?error=Username+already+taken", status_code=303
        )
    # Create the user; in production hash the password properly
    user = User(username=username, password=get_password_hash(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return RedirectResponse(url="/login", status_code=303)


@app.post("/chats/logout")
async def logout():
    # Invalidate the token or clear the session
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie(key="access_token")
    return response


@app.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        return RedirectResponse(url="/login?error=Invalid+credentials", status_code=303)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "id": user.id}, expires_delta=access_token_expires
    )

    response = RedirectResponse(url="/chats", status_code=303)
    response.set_cookie(key="access_token", value=access_token, httponly=True)

    return response


@app.get("/chats")
async def chats_page(
    request: Request, token: str = Depends(get_token), db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("id")
        if user_id is None:
            LOG.error("Invalid token: user_id is None")
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        LOG.error("Invalid token during jwt.decode")
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        LOG.error("not found")
        raise HTTPException(status_code=401, detail="User not found")

    chats = (
        db.query(Chat)
        .filter(Chat.users.any(id=user_id))
        .order_by(Chat.last_message_datetime.desc())
        .all()
    )

    chat_data = []
    for chat in chats:
        # Retrieve the other participant's username
        other_user = next(
            (participant for participant in chat.users if participant.id != user_id),
            None,
        )
        chat_data.append(
            {
                "id": chat.id,
                "name": other_user.username if other_user else "Unknown",
                "last_message": list(chat.messages)[-1],
                "last_message_time": chat.last_message_datetime,
            }
        )

    return templates.TemplateResponse(
        "chats.html", {"request": request, "chats": chat_data}
    )


# Serve an individual chat page by chat_id


@app.get("/chat/{chat_id}")
async def chat_page(
    chat_id: str,
    request: Request,
    token: str = Depends(get_token),
    db: Session = Depends(get_db),
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Query the chat and verify that the user is a participant
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if not chat or not any(user.id == user_id for user in chat.users):
        raise HTTPException(status_code=403, detail="Access denied to this chat")

    # Get the other participant (assuming 2-person chats)
    other_user = next((user for user in chat.users if user.id != user_id), None)
    other_user_name = other_user.username if other_user else "Unknown"

    # Get messages ordered by sent_datetime (assuming Message has sent_datetime field)
    messages_query = (
        db.query(Message)
        .filter(Message.chat_id == chat_id)
        .order_by(Message.sent_datetime.asc())
        .all()
    )
    # Build message data with sender username (assumes Message model has sender_id and text)

    cache_key = f"chat:{chat_id}:messages"
    cached_messages = await redis_client.get(cache_key)

    if cached_messages:
        message_data = json.loads(cached_messages)
    else:
        # Your existing logic to build message_data from the DB
        message_data = []
        for msg in messages_query:
            sender = db.query(User).filter(User.id == msg.sender_id).first()
            message_data.append(
                {
                    "sender": sender.username if sender else "Unknown",
                    "sent_datetime": (
                        msg.sent_datetime.strftime("%Y-%m-%d %H:%M:%S")
                        if msg.sent_datetime
                        else ""
                    ),
                    "text": msg.text,
                }
            )
    # Cache the messages for 5 minutes (300 seconds)
    await redis_client.set(cache_key, json.dumps(message_data), ex=300)

    return templates.TemplateResponse(
        "chat.html",
        {
            "request": request,
            "chat_id": chat_id,
            "other_user_name": other_user_name,
            "messages": message_data,
        },
    )


@app.post("/chats/create")
async def create_chat(
    recipient_username: str = Form(...),
    token: str = Depends(get_token),
    db: Session = Depends(get_db),
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        active_user_id: int = payload.get("id")
        if active_user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    active_user = db.query(User).filter(User.id == active_user_id).first()
    if not active_user:

        raise HTTPException(status_code=401, detail="User not found")

    recipient = db.query(User).filter(User.username == recipient_username).first()
    if not recipient:
        # Redirect with an error message if the recipient is not found
        return RedirectResponse(url="/chats?error=User+not+found", status_code=303)

    # Create a new chat and add both active and recipient users (assumes a many-to-many relationship)
    new_chat = Chat(last_message_datetime=datetime.now())
    new_chat.users.append(active_user)
    new_chat.users.append(recipient)
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)

    # Create the initial message with creation text
    new_message = Message(
        chat_id=new_chat.id,
        sender_id=active_user.id,
        sent_datetime=datetime.now(),
        text="creation completed",
    )
    db.add(new_message)
    # Update chat's last_message_datetime with the initial message timestamp
    new_chat.last_message_datetime = datetime.now()
    db.commit()

    return RedirectResponse(url=f"/chat/{new_chat.id}", status_code=303)


# A simple connection manager for chat websockets
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
async def chat_websocket(
    websocket: WebSocket,
    chat_id: str,
    token: str = Query(...),
    db: Session = Depends(get_db),
):
    try:
        # Decode the token to extract user information
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        active_user_id: int = payload.get("id")
        if active_user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Verify the user participates in the chat
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if not chat or not any(user.id == active_user_id for user in chat.users):
        raise HTTPException(status_code=403, detail="Access denied to this chat")

    await manager.connect(chat_id, websocket)
    try:
        while True:
            # Wait for client to send a message
            data = await websocket.receive_text()

            # Store the message in the database
            new_message = Message(
                chat_id=chat_id,
                sender_id=active_user_id,
                sent_datetime=datetime.now(),
                text=data,
            )
            db.add(new_message)
            db.commit()
            await redis_client.delete(f"chat:{chat_id}:messages")

            # Broadcast the new message to all connected clients in the chat
            await manager.broadcast(chat_id, data)
    except WebSocketDisconnect:
        manager.disconnect(chat_id, websocket)
