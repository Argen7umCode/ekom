from db.db import FormFinder, FormEmbedder
import os
import motor.motor_asyncio



db_path = os.environ.get("DATABASE_PATH")
db_name = os.environ.get("DATABASE_NAME")
collection_name = os.environ.get("COLLECTION_NAME")
db_username = os.environ.get("DATABASE_USERNAME")
db_password = os.environ.get("DATABASE_PASSWORD")

client = motor.motor_asyncio.AsyncIOMotorClient(db_path, 
                                                username=db_username, 
                                                password=db_password)
form_finder = FormFinder(client, db_name, collection_name)
form_embedder = FormEmbedder(client, db_name, collection_name)