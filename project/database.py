import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorGridFSBucket
from fastapi import Depends
import os


async def get_db():
    mongo_uri = os.getenv("MONGODB_URI")
    if not mongo_uri:
        raise ValueError("MONGODB_URI is not set in environment variables")
    #Create an AsyncIOMotorClient instance:
    client = motor.motor_asyncio.AsyncIOMotorClient(mongo_uri)
    return client.multimedia_db


#Create an AsyncIOMotorGridFSBucket instance for each GridFS bucket:
async def get_fs_audio(db=Depends(get_db)):
    return AsyncIOMotorGridFSBucket(db, bucket_name="audio")

async def get_fs_sprite(db=Depends(get_db)):
    return AsyncIOMotorGridFSBucket(db, bucket_name="sprite")