#(©)CodeXBotz
#recoded by @Its_Oreki_Hotarou


import pymongo, os
from config import DB_URI, DB_NAME


dbclient = pymongo.MongoClient(DB_URI)
database = dbclient[DB_NAME]

# Database collections
user_data = database['users']
premium_user = database['premium']


# User functions
async def present_user(user_id: int):
    found = user_data.find_one({'_id': user_id})
    return bool(found)


async def add_user(user_id: int):
    user_data.insert_one({'_id': user_id})
    return


async def full_userbase():
    user_docs = user_data.find()
    user_ids = []
    for doc in user_docs:
        user_ids.append(doc['_id'])

    return user_ids


async def del_user(user_id: int):
    user_data.delete_one({'_id': user_id})
    return


# Premium user functions
async def is_premium(user_id: int):
    found = premium_user.find_one({'_id': user_id})
    return bool(found)


async def add_premium(user_id: int):
    premium_user.insert_one({'_id': user_id})
    return


async def get_premium_users():
    premium_docs = premium_user.find()
    premium_ids = []
    for doc in premium_docs:
        premium_ids.append(doc['_id'])

    return premium_ids


async def remove_premium(user_id: int):
    premium_user.delete_one({'_id': user_id})
    return
