# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load environment variables from .env
load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('DATABASE_USER')}:" \
               f"{os.getenv('DATABASE_PASSWORD')}@" \
               f"{os.getenv('DATABASE_HOST')}:" \
               f"{os.getenv('DATABASE_PORT')}/" \
               f"{os.getenv('DATABASE_NAME')}"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
