from copy import copy
from typing import List


class Finder:
    def __init__(self, client,  db_name, collection_name):
        self.collection = client[db_name][collection_name]

    async def find_one(self, query: dict):
        data = (await self.collection.find_one(query))
        return {key : value for key, value in 
                data.items() if key != "_id"}

    async def find_many(self, query: dict):
        cursor = await self.collection.find(query)
        return await cursor.to_list()

class FormFinder(Finder):
    def __init__(self, client, db_name, collection_name):
        super().__init__(client, db_name, collection_name)

    async def get_form_by_fields(self, fields: dict):
        return await self.find_one(fields)

class Embedder:
    def __init__(self, client,  db_name, collection_name):
        self.collection = client[db_name][collection_name]
    
    async def insert_one(self, document: dict):
        return await self.collection.insert_one(document)

    async def insert_many(self, documents: List[dict]):
        return await self.collection.insert_many(documents)
    
class FormEmbedder(Embedder):
    def __init__(self, client, db_name, collection_name):
        super().__init__(client, db_name, collection_name)

    async def add_form(self, form_name: str, fields: dict):
        data = {"name" : form_name} | fields
        await self.insert_one(copy(data))
        return data

        