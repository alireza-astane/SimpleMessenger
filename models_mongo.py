from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from uuid import UUID
import uuid


class UserModel(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    username: str
    password: str


class ChatModel(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    last_message_datetime: datetime
    participants: List[UUID]


class MessageModel(BaseModel):
    chat_id: UUID
    sent_datetime: datetime
    sender_id: UUID
    text: str


class UserChatsModel(BaseModel):
    user_id: UUID
    chat_id: UUID
    last_message_datetime: datetime
