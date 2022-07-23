import pymongo
from pydantic import BaseModel
client = pymongo.MongoClient(
    "mongodb://localhost:27017/", username='azka', password='1415')
mydb = client['pymongo']
mycol = mydb['notes']


class Note(BaseModel):
    title: str
    description: str


notes = []
garage = [{
    'title': 'feet',
    'description': 'feet'
}, {
    'title': 'azka',
    "description": 'i love feet'
}]

for doc in garage:
    print(doc)
    notes.append(Note(**doc))

insert = mycol.insert_many(garage)
for x in mycol.find():
    print(x)
