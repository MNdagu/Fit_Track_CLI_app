from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from setup import Base, get_session

class Workout(Base):
    __tablename__ = 'workouts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # ForeignKey added
    workout_type = Column(String, nullable=False)
    workout_date = Column(Date, nullable=False)

    user = relationship("User", back_populates="workouts")
    exercises = relationship('Exercise', back_populates='workout')

    def save(self):
        session = get_session()
        session.add(self)
        session.commit()

    @classmethod
    def find_by_user(cls, user_id):
        session = get_session()
        return session.query(cls).filter_by(user_id=user_id).all()

    @classmethod
    def delete(cls, workout_id):
        session = get_session()
        session.query(cls).filter_by(id=workout_id).delete()
        session.commit()
