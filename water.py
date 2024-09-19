#water.py

from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from setup import Base

class WaterIntake(Base):
    __tablename__ = 'water_intakes'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)
    
    def __repr__(self):
        return f"<WaterIntake(id={self.id}, user_id={self.user_id}, date={self.date}, amount={self.amount} liters)>"
