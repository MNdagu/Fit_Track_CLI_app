#report.py

from tabulate import tabulate
from setup import get_session
from user import User
from workout import Workout
from meal import Meal
from water import WaterIntake
from exercise import Exercise

class Report:
    def __init__(self, user_id):
        self.user_id = user_id

    def generate(self):
        session = get_session()
        user = session.query(User).filter_by(id=self.user_id).first()
        if not user:
            return "User not found."

        workouts = session.query(Workout).filter_by(user_id=self.user_id).all()
        meals = session.query(Meal).filter_by(user_id=self.user_id).all()
        water_intakes = session.query(WaterIntake).filter_by(user_id=self.user_id).all()
        
        # Formatting Workouts
        workout_data = []
        for w in workouts:
            exercises = session.query(Exercise).filter_by(workout_id=w.id).all()
            for e in exercises:
                workout_data.append((w.workout_type, w.workout_date, e.exercise_name, e.sets, e.reps, e.weight))
        workout_table = tabulate(workout_data, headers=["Workout Type", "Date", "Exercise", "Sets", "Reps", "Weight (kg)"], tablefmt="grid")

        # Formatting Meals
        meal_data = [(m.meal_type, m.calories, m.protein, m.carbs, m.fats) for m in meals]
        meal_table = tabulate(meal_data, headers=["Meal Type", "Calories", "Protein (g)", "Carbs (g)", "Fats (g)"], tablefmt="grid")

        # Formatting Water Intake
        water_data = [(w.date, w.amount) for w in water_intakes]
        water_table = tabulate(water_data, headers=["Date", "Amount (L)"], tablefmt="grid")

        report = f"\n---Report for User {self.user_id}---\n\n"
        report += "Workouts:\n"
        report += workout_table + "\n\n"
        report += "Meals:\n"
        report += meal_table + "\n\n"
        report += "Water Intake:\n"
        report += water_table

        return report
