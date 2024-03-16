from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Define the base model
Base = declarative_base()

# Define the Prediction model
class Prediction(Base):
    __tablename__ = 'prediction'
    id = Column(Integer, primary_key=True)
    # Add your prediction fields here

# Specify the full path to the database file
db_path = r'D:\website-recommendations-code\instance\recommendations.db'

# Database URL (SQLite in this case)
db_url = f'sqlite:///{db_path}'

# Create an engine and connect to the database
engine = create_engine(db_url)

# Create all tables
Base.metadata.create_all(engine)

print("Prediction table created successfully.")
