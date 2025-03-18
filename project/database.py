import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient("your_mongo_connection_string")
db = client.multimedia_db