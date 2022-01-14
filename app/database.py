# Only needed if connect to Postgres via Postgres database driver
# import time
# import psycopg2
# from psycopg2.extras import RealDictCursor


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@" \
                          f"{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CONNECT TO POSTGRES DATABASE USING POSTGRES DATABASE DRIVER
# while True:
#     try:
#         # Connect to your postgres DB
#         conn = psycopg2.connect(
#             database="fastapi", user="gareth", password="letmein", host='localhost', cursor_factory=RealDictCursor)
#         # Open a cursor to perform database operations
#         cursor = conn.cursor()
#         print('Database connection successful')
#         break
#     except Exception as e:
#         print(f'connection to database failed because of {e}')
#         time.sleep(2)
