#meal.py

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from setup import Base

class Meal(Base):
    __tablename__ = 'meals'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    meal_type = Column(String, nullable=False)
    calories = Column(Float, nullable=False)
    protein = Column(Float, nullable=False)
    carbs = Column(Float, nullable=False)
    fats = Column(Float, nullable=False)
    
    def __repr__(self):
        return (f"<Meal(id={self.id}, user_id={self.user_id}, type='{self.meal_type}', calories={self.calories}, "
                f"protein={self.protein}, carbs={self.carbs}, fats={self.fats})>")

