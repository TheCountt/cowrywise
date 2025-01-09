import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mongodb://localhost/mydb")
    RABBITMQ_HOST: str = os.getenv("RABBITMQ_HOST", "localhost")
    RABBITMQ_QUEUE: str = os.getenv("RABBITMQ_QUEUE", "default_queue")

settings = Settings()