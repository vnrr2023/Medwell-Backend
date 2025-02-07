import os
from dotenv import load_dotenv
load_dotenv()

class Secret:
    MONGO_USER = os.environ["MONGO_USER"]
    MONGO_PASSWORD = os.environ["MONGO_PASS"]
    HOST=os.environ["DB_HOST"]
    DB_NAME=os.environ["DB_NAME"]
    USER=os.environ["USER"]
    PASSWORD=os.environ["PASSWORD"]
    REDIS_URI=os.environ["REDIS_URI"]
    GROQ_KEY=os.environ['GROQ']
