import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = os.getenv('MONGO_URI')
    MONGO_DBNAME = os.getenv('MONGO_DBNAME')
    MONGO_DBNAME_MODELS = os.getenv('MONGO_DBNAME_MODELS')