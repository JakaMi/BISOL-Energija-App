from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

# DATABASE_URL = "sqlite:///./energy_data.db"

# Create the engine
engine = create_engine(DATABASE_URL, echo=True)

# SessionLocal will be used to create new sessions for each request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the tables in the database
def create_db():
    SQLModel.metadata.create_all(engine)

# Dependency function to get the DB session for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# DATABASE_URL = "sqlite:///./energy_data.db"  # Za razvoj SQLite, v produkciji PostgreSQL

# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# # SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# # Base = declarative_base()


# def init_db():
#     SQLModel.metadata.create_all(engine)

# def get_session():
#     with Session(engine) as session:
#         yield session
        
# SessionDep = Annotated[Session, Depends(get_session)]

# # def get_db():
# #     db = SessionLocal()
# #     try:
# #         yield db
# #     finally:
# #         db.close()
