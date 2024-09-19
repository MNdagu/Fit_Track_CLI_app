#workout.py

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from setup import Base

class Workout(Base):
    __tablename__ = 'workouts'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    workout_type = Column(String, nullable=False)
    workout_date = Column(Date, nullable=False)
    
    exercises = relationship('Exercise', back_populates='workout')
    
    def __repr__(self):
        return f"<Workout(id={self.id}, user_id={self.user_id}, type='{self.workout_type}', date={self.workout_date})>"

