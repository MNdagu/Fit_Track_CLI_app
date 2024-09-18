
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date, DateTime, func
from sqlalchemy.orm import relationship
from setup import Base, get_session
from datetime import datetime

class Exercise(Base):
    __tablename__ = 'exercises'
    
    id = Column(Integer, primary_key=True)
    workout_id = Column(Integer, ForeignKey('workouts.id'))
    exercise_name = Column(String)
    sets = Column(Integer)
    reps = Column(Integer)
    weight = Column(Float)
    created_at = Column(DateTime, default=func.now())

    workout = relationship('Workout', back_populates='exercises')

    def save(self):
        session = get_session()
        session.add(self)
        session.commit()

    @classmethod
    def find_by_workout(cls, workout_id):
        session = get_session()
        return session.query(cls).filter_by(workout_id=workout_id).all()

    @classmethod
    def delete(cls, exercise_id):
        session = get_session()
        session.query(cls).filter_by(id=exercise_id).delete()
        session.commit()