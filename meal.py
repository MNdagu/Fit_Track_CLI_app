from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from setup import Base, get_session

class Meal(Base):
    __tablename__ = 'meals'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    meal_type = Column(String)
    calories = Column(Float)
    protein = Column(Float)
    carbs = Column(Float)
    fats = Column(Float)

    user = relationship('User', back_populates='meals')

    def save(self):
        session = get_session()
        session.add(self)
        session.commit()

    @classmethod
    def find_by_user(cls, user_id):
        session = get_session()
        return session.query(cls).filter_by(user_id=user_id).all()

    @classmethod
    def delete(cls, meal_id):
        session = get_session()
        session.query(cls).filter_by(id=meal_id).delete()
        session.commit()
