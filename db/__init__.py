from db.db import FormFinder, FormEmbedder
import motor.motor_asyncio

db_path = 'mongodb://localhost:27017'
db_name = 'ekom'
collection_name = 'forms'

client = motor.motor_asyncio.AsyncIOMotorClient(db_path)
form_finder = FormFinder(client, db_name, collection_name)
form_embedder = FormEmbedder(client, db_name, collection_name)