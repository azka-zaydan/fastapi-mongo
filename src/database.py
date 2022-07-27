from fastapi import HTTPException
from pymongo import MongoClient
from models import NoteResult
from datetime import datetime
from util import hashpass, verify
from pymongo.errors import DuplicateKeyError

mongo = MongoClient(
    "mongodb://localhost:27017/", username='azka', password='1415')

database = mongo['noteapp']

notes_collection = database['notes']
users_collection = database['users']
users_collection.create_index('email', unique=True)


async def fetch_all(current_user: str):
    notes = []
    cursor = notes_collection.find({'owner': current_user})
    for doc in cursor:
        notes.append(
            NoteResult(**doc))
    return notes


async def fetch_by_title(title: str, current_user: str):
    return notes_collection.find_one({"title": title, "owner": current_user})


async def update_note(title: str, description: str, current_user: str):
    await notes_collection.update_one({'title': title, 'owner': current_user}, {"$set": {"description": description}})
    return notes_collection.find_one({"title": title})


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
    try:
        users_collection.insert_one(user)
    except DuplicateKeyError:
        raise HTTPException(404, 'User already exist')
    return user


async def find_user(email: str):
    return users_collection.find_one({"email": email})


async def change_user_password(passwords: dict, current_user: str):
    find = users_collection.find_one({"email": current_user})

    if find:
        if verify(passwords['old_password'], find['password']):
            new_pass = hashpass(passwords['new_password'])
            users_collection.update_one({"email": current_user}, {
                                        '$set': {'password': new_pass}})
            return "Password Updated"
        return None
    return None


async def delete_user(email: str):
    find = users_collection.find_one({'email': email})
    if find:
        users_collection.delete_one({"email": email})
        notes_collection.delete_many({"owner": email})
        return "User gone"
    return None
