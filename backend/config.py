import os
from dotenv import load_dotenv


load_dotenv(".env")

class Config:
    MONGO_URI = os.environ["MONGO_CONN_URI"]
