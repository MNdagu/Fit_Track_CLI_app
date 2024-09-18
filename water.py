from sqlalchemy import Column, Integer, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from setup import Base, get_session

class WaterIntake(Base):
    __tablename__ = 'water_intakes'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)  # Float for liters of water

    user = relationship("User", back_populates="water_intakes")

    def save(self):
        session = get_session()
        session.add(self)
        session.commit()

    @classmethod
    def find_by_user(cls, user_id):
        session = get_session()
        return session.query(cls).filter_by(user_id=user_id).all()

    @classmethod
    def delete(cls, intake_id):
        session = get_session()
        session.query(cls).filter_by(id=intake_id).delete()
        session.commit()
