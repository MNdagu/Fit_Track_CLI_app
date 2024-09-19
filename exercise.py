#exercise.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from setup import Base

class Exercise(Base):
    __tablename__ = 'exercises'
    
    id = Column(Integer, primary_key=True)
    workout_id = Column(Integer, ForeignKey('workouts.id'), nullable=False)
    exercise_name = Column(String, nullable=False)
    sets = Column(Integer, nullable=False)
    reps = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    
    workout = relationship('Workout', back_populates='exercises')
    
    def __repr__(self):
        return (f"<Exercise(id={self.id}, workout_id={self.workout_id}, name='{self.exercise_name}', "
                f"sets={self.sets}, reps={self.reps}, weight={self.weight})>")
