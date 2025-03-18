import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorGridFSBucket

#Create an AsyncIOMotorClient instance:
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://josefcarlmuscat4:0QxQeZsHKhaT1RJ7@josefmuscatdgdhomede.x9fju.mongodb.net/?retryWrites=true&w=majority&appName=JOSEFMUSCATDGDHOMEDE")
db = client.multimedia_db # Create a database instance

#Create an AsyncIOMotorGridFSBucket instance for each GridFS bucket:
fs_audio = AsyncIOMotorGridFSBucket(db, bucket_name="audio") # Create an instance for the audio bucket
fs_sprite = AsyncIOMotorGridFSBucket(db, bucket_name="sprite") # Create an instance for the sprite bucket