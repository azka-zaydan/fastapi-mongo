from fastapi import Depends
from pymongo import MongoClient
from models import Note, NoteResult
from datetime import datetime
from oauth2 import get_current_user
from util import hashpass


mongo = MongoClient(
    "mongodb://localhost:27017/", username='azka', password='1415')

database = mongo['pymongo']

notes_collection = database['notes']
users_collection = database['users']


async def fetch_all(current_user: str):
    notes = []
    cursor = notes_collection.find({'owner': current_user})
    for doc in cursor:
        notes.append(
            NoteResult(**doc))
    return notes


async def fetch_by_title(title: str, current_user: str):
    cursor = notes_collection.find_one({"title": title, "owner": current_user})
    return cursor


async def update_note(title: str, description: str, current_user: str):
    await notes_collection.update_one({'title': title, 'owner': current_user}, {"$set": {"description": description}})
    document = notes_collection.find_one({"title": title})
    return document


async def remove_note(title: str, current_user: str):
    notes_collection.delete_one({"title": title, 'owner': current_user})
    return True


async def create_note(note: dict, current_user: str):
    note['created_at'] = datetime.now()
    note['owner'] = current_user
    notes_collection.insert_one(note)
    return note


async def create_user(user: dict):
    user['password'] = hashpass(user['password'])
    user['created_at'] = datetime.now()
    # print(type(user))
    user_exist = users_collection.find_one({"email": user['email']})
    if user_exist:
        return None
    users_collection.insert_one(user)
    return user


async def find_user(email: str):
    cursor = users_collection.find_one({"email": email})
    return cursor
