from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from setup import Base, get_session
from user import User
from workout import Workout
from meal import Meal
from water import WaterIntake

class Report(Base):
    __tablename__ = 'reports'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    report_date = Column(Date, nullable=False)
    workout_summary = Column(String)
    meal_summary = Column(String)
    water_summary = Column(String)

    user = relationship("User")

    def save(self):
        session = get_session()
        session.add(self)
        session.commit()

    @classmethod
    def find_by_user(cls, user_id):
        session = get_session()
        return session.query(cls).filter_by(user_id=user_id).all()

    def generate(self):
        # Example of generating a simple report
        session = get_session()
        user = session.query(User).filter_by(id=self.user_id).first()
        if not user:
            return "User not found."

        workouts = session.query(Workout).filter_by(user_id=self.user_id).all()
        meals = session.query(Meal).filter_by(user_id=self.user_id).all()
        water_intakes = session.query(WaterIntake).filter_by(user_id=self.user_id).all()

        report = f"Report for User {self.user_id}\n"
        report += "Workouts:\n"
        for workout in workouts:
            report += f" - {workout.workout_type} on {workout.workout_date}\n"
        
        report += "Meals:\n"
        for meal in meals:
            report += f" - {meal.meal_type}: {meal.calories} calories\n"
        
        report += "Water Intake:\n"
        for water in water_intakes:
            report += f" - {water.date}: {water.amount} liters\n"

        return report
