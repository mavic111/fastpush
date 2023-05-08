from sqlmodel import create_engine
import os
from dotenv.main import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# sqlite_file_name = "database.db"
# sqlite_url = f"sqlite:///{sqlite_file_name}"

# connect_args = {"check_same_thread": False}
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
