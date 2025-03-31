from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

# Association table for many-to-many relationship between Users and Chats
user_chat_association = Table(
    "user_chat_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("chat_id", Integer, ForeignKey("chats.id")),
)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    # A user can belong to many chats
    chats = relationship(
        "Chat", secondary=user_chat_association, back_populates="users"
    )


class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True, index=True)
    last_message_datetime = Column(DateTime)
    # One chat can have many messages
    messages = relationship("Message", back_populates="chat")
    # A chat can be between many users
    users = relationship(
        "User", secondary=user_chat_association, back_populates="chats"
    )


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    sent_datetime = Column(DateTime)
    text = Column(Text)
    # Relationship to chat
    chat = relationship("Chat", back_populates="messages")
