import psycopg2
from app.core.config import settings

def get_db_client():
    return psycopg2.connect(settings.DATABASE_URL)
