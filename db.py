import motor.motor_asyncio
from datetime import datetime


client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')

db = client['ekom']
collection = db['templates']


class Collection(motor.motor_asyncio.AsyncIOMotorClient):
    def __init__(self, db_name, collection_name):
        self.collection = self[db_name][collection_name]

class Finder(Collection):
    def __init__(self, db_name, collection_name):
        super().__init__(db_name, collection_name)

    async def find_one(self, query: dict):
        return await self.collection.find_one(query)

    async def find_many(self, query: dict):
        cursor = await self.collection.find(query)
        return await cursor.to_list()

class TemplateFinder(Finder):
    def __init__(self, db_name, collection_name):
        super().__init__(db_name, collection_name)

    async def get_template_by_name_and_fields(self, template_name: str, fields: dict):
        query = {'name' : template_name} | fields
        return self.find_one(query)

