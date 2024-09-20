#cli.py

from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from setup import get_session
from user import User
from workout import Workout
from exercise import Exercise
from meal import Meal
from water import WaterIntake
from report import Report
from tabulate import tabulate


# User Functions
def create_user():
    try:
        username = input("Enter username: ").strip()
        if not username:
            print("Username cannot be empty.")
            return

        with get_session() as session:
            user = User(username=username)
            session.add(user)
            session.commit()
            print(f"User '{username}' created successfully.")
    except SQLAlchemyError as e:
        print(f"Error creating user: {e}")


def view_all_users():
    try:
        with get_session() as session:
            users = session.query(User).all()
            if users:
                user_data = [(user.id, user.username) for user in users]
                headers = ["ID", "Username"]
                print(tabulate(user_data, headers=headers, tablefmt="grid"))
            else:
                print("No users found.")
    except SQLAlchemyError as e:
        print(f"Error viewing users: {e}")


def find_user_by_id():
    try:
        user_id = input("Enter user ID: ").strip()
        if not user_id.isdigit():
            print("Invalid ID. Please enter a numeric value.")
            return

        user_id = int(user_id)
        with get_session() as session:
            user = session.query(User).filter_by(id=user_id).first()
            if user:
                user_data = [(user.id, user.username)]
                headers = ["ID", "Username"]
                print(tabulate(user_data, headers=headers, tablefmt="grid"))
            else:
                print("User not found.")
    except SQLAlchemyError as e:
        print(f"Error finding user: {e}")


def delete_user():
    try:
        user_id = input("Enter user ID to delete: ").strip()
        if not user_id.isdigit():
            print("Invalid ID. Please enter a numeric value.")
            return

        user_id = int(user_id)
        with get_session() as session:
            user = session.query(User).filter_by(id=user_id).first()
            if user:
                session.delete(user)
                session.commit()
                print(f"User with ID {user_id} deleted successfully.")
            else:
                print("User not found.")
    except SQLAlchemyError as e:
        print(f"Error deleting user: {e}")


# Workout Functions
def add_workout():
    try:
        user_id = input("Enter user ID: ").strip()
        if not user_id.isdigit():
            print("Invalid ID. Please enter a numeric value.")
            return

        user_id = int(user_id)
        workout_type = input("Enter workout type: ").strip()
        workout_date_str = input("Enter workout date (YYYY-MM-DD): ").strip()
        try:
            workout_date = datetime.strptime(workout_date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please enter in YYYY-MM-DD format.")
            return

        with get_session() as session:
            new_workout = Workout(user_id=user_id, workout_type=workout_type, workout_date=workout_date)
            session.add(new_workout)
            session.commit()
            print("Workout added successfully.")
    except Exception as e:
        print(f"Error adding workout: {e}")


def view_workouts():
    try:
        with get_session() as session:
            workouts = session.query(Workout).all()
            if workouts:
                workout_data = [(workout.id, workout.user_id, workout.workout_type, workout.workout_date) for workout in workouts]
                headers = ["ID", "User ID", "Workout Type", "Date"]
                print(tabulate(workout_data, headers=headers, tablefmt="grid"))
            else:
                print("No workouts found.")
    except SQLAlchemyError as e:
        print(f"Error viewing workouts: {e}")


# Exercise Functions
def add_exercise():
    try:
        workout_id = input("Enter workout ID: ").strip()
        if not workout_id.isdigit():
            print("Invalid ID. Please enter a numeric value.")
            return

        workout_id = int(workout_id)
        exercise_name = input("Enter exercise name: ").strip()
        sets_str = input("Enter number of sets: ").strip()
        reps_str = input("Enter number of reps per set: ").strip()
        weight_str = input("Enter weight (in kg): ").strip()

        # Validate numeric inputs
        try:
            sets = int(sets_str)
            reps = int(reps_str)
            weight = float(weight_str)
        except ValueError:
            print("Invalid input. Please enter valid numbers for sets, reps, and weight.")
            return

        with get_session() as session:
            exercise = Exercise(workout_id=workout_id, exercise_name=exercise_name, sets=sets, reps=reps, weight=weight)
            session.add(exercise)
            session.commit()
            print("Exercise added successfully.")
    except SQLAlchemyError as e:
        print(f"Error adding exercise: {e}")


def view_exercises():
    try:
        workout_id = input("Enter workout ID: ").strip()
        if not workout_id.isdigit():
            print("Invalid ID. Please enter a numeric value.")
            return

        workout_id = int(workout_id)
        with get_session() as session:
            exercises = session.query(Exercise).filter_by(workout_id=workout_id).all()
            if exercises:
                exercise_data = [(exercise.id, exercise.workout_id, exercise.exercise_name, exercise.sets, exercise.reps, exercise.weight) 
                                 for exercise in exercises]
                headers = ["ID", "Workout ID", "Exercise Name", "Sets", "Reps", "Weight"]
                print(tabulate(exercise_data, headers=headers, tablefmt="grid"))
            else:
                print("No exercises found for this workout.")
    except SQLAlchemyError as e:
        print(f"Error viewing exercises: {e}")


# Meal Functions
def log_meal():
    try:
        user_id = input("Enter user ID: ").strip()
        if not user_id.isdigit():
            print("Invalid ID. Please enter a numeric value.")
            return

        user_id = int(user_id)
        meal_type = input("Enter meal type: ").strip()
        calories_str = input("Enter calories: ").strip()
        protein_str = input("Enter protein (g): ").strip()
        carbs_str = input("Enter carbs (g): ").strip()
        fats_str = input("Enter fats (g): ").strip()

        # Validate numeric inputs
        try:
            calories = float(calories_str)
            protein = float(protein_str)
            carbs = float(carbs_str)
            fats = float(fats_str)
        except ValueError:
            print("Invalid input. Please enter valid numbers for calories, protein, carbs, and fats.")
            return

        with get_session() as session:
            meal = Meal(user_id=user_id, meal_type=meal_type, calories=calories, protein=protein, carbs=carbs, fats=fats)
            session.add(meal)
            session.commit()
            print("Meal logged successfully.")
    except SQLAlchemyError as e:
        print(f"Error logging meal: {e}")


def view_meal_history():
    try:
        with get_session() as session:
            meals = session.query(Meal).all()
            if meals:
                meal_data = [(meal.id, meal.user_id, meal.meal_type, meal.calories, meal.protein, meal.carbs, meal.fats)
                             for meal in meals]
                headers = ["ID", "User ID", "Meal Type", "Calories", "Protein (g)", "Carbs (g)", "Fats (g)"]
                print(tabulate(meal_data, headers=headers, tablefmt="grid"))
            else:
                print("No meal history found.")
    except SQLAlchemyError as e:
        print(f"Error viewing meal history: {e}")


# Water Intake Functions
def log_water_intake():
    try:
        user_id = input("Enter user ID: ").strip()
        if not user_id.isdigit():
            print("Invalid ID. Please enter a numeric value.")
            return

        user_id = int(user_id)
        date_str = input("Enter date (YYYY-MM-DD): ").strip()
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            print("Invalid date format. Please enter in YYYY-MM-DD format.")
            return

        amount_str = input("Enter amount of water (in liters): ").strip()
        try:
            amount = float(amount_str)
        except ValueError:
            print("Invalid input. Please enter a valid number for water amount.")
            return

        with get_session() as session:
            water_intake = WaterIntake(user_id=user_id, date=date_obj, amount=amount)
            session.add(water_intake)
            session.commit()
            print("Water intake logged successfully.")
    except SQLAlchemyError as e:
        print(f"Error logging water intake: {e}")


def view_water_intake():
    try:
        with get_session() as session:
            water_intakes = session.query(WaterIntake).all()
            if water_intakes:
                water_data = [(water.id, water.user_id, water.date, water.amount) for water in water_intakes]
                headers = ["ID", "User ID", "Date", "Amount (liters)"]
                print(tabulate(water_data, headers=headers, tablefmt="grid"))
            else:
                print("No water intake records found.")
    except SQLAlchemyError as e:
        print(f"Error viewing water intake: {e}")


# Report Function
def generate_report():
    try:
        user_id = input("Enter user ID for report: ").strip()
        if not user_id.isdigit():
            print("Invalid ID. Please enter a numeric value.")
            return

        user_id = int(user_id)
        with get_session() as session:
            report = Report(user_id=user_id)
            report_data = report.generate()
            print(report_data)
    except SQLAlchemyError as e:
        print(f"Error generating report: {e}")


# Menu Functions
def main_menu():
    while True:
        print("\nFitness Tracker CLI")
        print("1. User Management")
        print("2. Workout Management")
        print("3. Meal Management")
        print("4. Water Intake Management")
        print("5. Generate Report")
        print("6. Exit")
        choice = input("Choose an option: ").strip()

        if choice == '1':
            user_menu()
        elif choice == '2':
            workout_menu()
        elif choice == '3':
            meal_menu()
        elif choice == '4':
            water_menu()
        elif choice == '5':
            generate_report()
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


def user_menu():
    while True:
        print("\nUser Management")
        print("1. Create User")
        print("2. View All Users")
        print("3. Find User by ID")
        print("4. Delete User")
        print("5. Back to Main Menu")
        choice = input("Choose an option: ").strip()

        if choice == '1':
            create_user()
        elif choice == '2':
            view_all_users()
        elif choice == '3':
            find_user_by_id()
        elif choice == '4':
            delete_user()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")


def workout_menu():
    while True:
        print("\nWorkout Management")
        print("1. Add Workout")
        print("2. View Workouts")
        print("3. Add Exercise")
        print("4. View Exercises")
        print("5. Back to Main Menu")
        choice = input("Choose an option: ").strip()

        if choice == '1':
            add_workout()
        elif choice == '2':
            view_workouts()
        elif choice == '3':
            add_exercise()
        elif choice == '4':
            view_exercises()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please select a valid option.")


def meal_menu():
    while True:
        print("\nMeal Management")
        print("1. Log Meal")
        print("2. View Meal History")
        print("3. Back to Main Menu")
        choice = input("Choose an option: ").strip()

        if choice == '1':
            log_meal()
        elif choice == '2':
            view_meal_history()
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")


def water_menu():
    while True:
        print("\nWater Intake Management")
        print("1. Log Water Intake")
        print("2. View Water Intake")
        print("3. Back to Main Menu")
        choice = input("Choose an option: ").strip()

        if choice == '1':
            log_water_intake()
        elif choice == '2':
            view_water_intake()
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main_menu()
