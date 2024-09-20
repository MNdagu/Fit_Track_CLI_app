#setup.py 
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

Base = declarative_base()

def get_db_url():
    return f"sqlite:///{os.path.join(os.path.dirname(__file__), 'fitness_tracker.db')}"

def get_engine():
    return create_engine(get_db_url(), echo=True)

def get_session():
    Session = sessionmaker(bind=get_engine())
    return Session()

def create_tables():
    # Import models here
    from user import User
    from workout import Workout
    from exercise import Exercise
    from meal import Meal
    from water import WaterIntake
    from report import Report
    
    engine = get_engine()
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    create_tables()
