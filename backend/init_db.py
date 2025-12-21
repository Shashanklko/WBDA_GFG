from sqlalchemy import create_engine
from app.core.config import settings
from app.db.models import Base
from sqlalchemy_utils import database_exists, create_database

def init_db():
    engine = create_engine(settings.DATABASE_URL)
    if not database_exists(engine.url):
        create_database(engine.url)
        print(f"Created database {settings.DATABASE_URL}")
    else:
        print(f"Database {settings.DATABASE_URL} already exists")

    Base.metadata.create_all(bind=engine)
    print("Tables created.")

if __name__ == "__main__":
    init_db()
