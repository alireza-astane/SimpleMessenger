import motor.motor_asyncio

MONGO_DETAILS = "mongodb://localhost:27017/?uuidRepresentation=standard"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client.messenger

# Collections
users_collection = database.get_collection("users")
chats_collection = database.get_collection("chats")
messages_collection = database.get_collection("messages")
user_chats_collection = database.get_collection("user_chats")
