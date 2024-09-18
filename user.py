from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from setup import Base, get_session

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())

    workouts = relationship("Workout", back_populates="user")
    meals = relationship('Meal', back_populates='user')
    water_intakes = relationship('WaterIntake', back_populates='user')

    def save(self):
        session = get_session()
        session.add(self)
        session.commit()

    @classmethod
    def all(cls):
        session = get_session()
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, user_id):
        session = get_session()
        return session.query(cls).filter_by(id=user_id).first()

    @classmethod
    def delete(cls, user_id):
        session = get_session()
        session.query(cls).filter_by(id=user_id).delete()
        session.commit()
