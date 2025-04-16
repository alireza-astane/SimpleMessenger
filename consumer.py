from kafka import KafkaConsumer
import json
from datetime import datetime
import asyncio
from uuid import UUID
import motor.motor_asyncio

# Initialize a KafkaConsumer.
consumer = KafkaConsumer(
    "chat_messages",
    bootstrap_servers=["localhost:9092"],
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    auto_offset_reset="earliest",
    enable_auto_commit=True,
)

# Initialize Mongo client (adjust as needed)
client = motor.motor_asyncio.AsyncIOMotorClient(
    "mongodb://localhost:27017/", uuidRepresentation="standard"
)
db = client.messenger


async def process_message(message):
    data = message.value
    chat_id = data["chat_id"]
    # Insert the message
    await db.messages.insert_one(
        {
            "chat_id": UUID(chat_id),
            "sender_id": UUID(data["sender_id"]),
            "sent_datetime": datetime.fromisoformat(data["sent_datetime"]),
            "text": data["text"],
        }
    )

    await db.chats.update_one(
        {"id": UUID(chat_id)},
        {
            "$set": {
                "last_message_datetime": datetime.fromisoformat(data["sent_datetime"])
            }
        },
    )
    print(f"Processed message: {data}")


async def consume():
    for message in consumer:
        await process_message(message)


if __name__ == "__main__":
    asyncio.run(consume())
