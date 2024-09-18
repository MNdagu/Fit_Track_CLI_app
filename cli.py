# cli.py

from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
# from models.user import User
from workout import Workout
from exercise import Exercise
from meal import Meal
# from models.report import Report
from water import WaterIntake
# from models.setup import get_session
from datetime import datetime

from setup import get_session, create_tables



# Function Definitions

def create_user():
    from user import User

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
    from user import User

    try:
        with get_session() as session:
            users = session.query(User).all()
            if users:
                for user in users:
                    print(f"ID: {user.id}, Username: {user.username}")
            else:
                print("No users found.")
    except SQLAlchemyError as e:
        print(f"Error viewing users: {e}")

def find_user_by_id():
    from user import User

    try:
        user_id = input("Enter user ID: ").strip()
        if not user_id.isdigit():
            print("Invalid ID. Please enter a numeric value.")
            return

        with get_session() as session:
            user = session.query(User).filter_by(id=int(user_id)).first()
            if user:
                print(f"ID: {user.id}, Username: {user.username}")
            else:
                print("User not found.")
    except SQLAlchemyError as e:
        print(f"Error finding user: {e}")

def delete_user():
    from user import User
    try:
        user_id = input("Enter user ID to delete: ").strip()
        if not user_id.isdigit():
            print("Invalid ID. Please enter a numeric value.")
            return

        with get_session() as session:
            user = session.query(User).filter_by(id=int(user_id)).first()
            if user:
                session.delete(user)
                session.commit()
                print(f"User with ID {user_id} deleted successfully.")
            else:
                print("User not found.")
    except SQLAlchemyError as e:
        print(f"Error deleting user: {e}")

def add_workout():
    session = get_session()

    try:
        user_id = int(input("Enter user ID: "))
        workout_type = input("Enter workout type: ")
        workout_date_str = input("Enter workout date (YYYY-MM-DD): ")

        # Convert the date string to a date object
        workout_date = datetime.strptime(workout_date_str, "%Y-%m-%d").date()

        # Create a new Workout instance
        new_workout = Workout(
            user_id=user_id,
            workout_type=workout_type,
            workout_date=workout_date
        )

        # Add and commit the new workout
        session.add(new_workout)
        session.commit()
        print("Workout added successfully.")
    except Exception as e:
        session.rollback()
        print(f"Error adding workout: {e}")
    finally:
        session.close()

def view_workouts():
    try:
        with get_session() as session:
            workouts = session.query(Workout).all()
            if workouts:
                for workout in workouts:
                    print(f"ID: {workout.id}, User ID: {workout.user_id}, Type: {workout.workout_type}, Date: {workout.workout_date}")
            else:
                print("No workouts found.")
    except SQLAlchemyError as e:
        print(f"Error viewing workouts: {e}")

def add_exercise():
    try:
        workout_id = input("Enter workout ID: ").strip()
        if not workout_id.isdigit():
            print("Invalid ID. Please enter a numeric value.")
            return

        exercise_name = input("Enter exercise name: ").strip()
        sets = int(input("Enter number of sets: ").strip())
        reps = int(input("Enter number of reps per set: ").strip())
        weight = float(input("Enter weight (in kg): ").strip())

        with get_session() as session:
            exercise = Exercise(workout_id=int(workout_id), exercise_name=exercise_name, sets=sets, reps=reps, weight=weight)
            session.add(exercise)
            session.commit()
            print("Exercise added successfully.")
    except ValueError:
        print("Invalid input. Please enter numerical values correctly.")
    except SQLAlchemyError as e:
        print(f"Error adding exercise: {e}")

def view_exercises():
    try:
        workout_id = input("Enter workout ID: ").strip()
        if not workout_id.isdigit():
            print("Invalid ID. Please enter a numeric value.")
            return

        with get_session() as session:
            exercises = session.query(Exercise).filter_by(workout_id=int(workout_id)).all()
            if exercises:
                for exercise in exercises:
                    print(f"ID: {exercise.id}, Workout ID: {exercise.workout_id}, Name: {exercise.exercise_name}, Sets: {exercise.sets}, Reps: {exercise.reps}, Weight: {exercise.weight}")
            else:
                print("No exercises found for this workout.")
    except SQLAlchemyError as e:
        print(f"Error viewing exercises: {e}")

def log_meal():
    try:
        user_id = input("Enter user ID: ").strip()
        if not user_id.isdigit():
            print("Invalid ID. Please enter a numeric value.")
            return

        meal_type = input("Enter meal type: ").strip()
        calories = float(input("Enter calories: ").strip())
        protein = float(input("Enter protein (g): ").strip())
        carbs = float(input("Enter carbs (g): ").strip())
        fats = float(input("Enter fats (g): ").strip())

        with get_session() as session:
            meal = Meal(user_id=int(user_id), meal_type=meal_type, calories=calories, protein=protein, carbs=carbs, fats=fats)
            session.add(meal)
            session.commit()
            print("Meal logged successfully.")
    except ValueError:
        print("Invalid input. Please enter numerical values correctly.")
    except SQLAlchemyError as e:
        print(f"Error logging meal: {e}")

def view_meal_history():
    try:
        with get_session() as session:
            meals = session.query(Meal).all()
            if meals:
                for meal in meals:
                    print(f"ID: {meal.id}, User ID: {meal.user_id}, Type: {meal.meal_type}, Calories: {meal.calories}, Protein: {meal.protein}, Carbs: {meal.carbs}, Fats: {meal.fats}")
            else:
                print("No meal history found.")
    except SQLAlchemyError as e:
        print(f"Error viewing meal history: {e}")

def log_water_intake():
    user_id = int(input("Enter user ID: "))
    date_str = input("Enter date (YYYY-MM-DD): ")
    amount = float(input("Enter amount of water (in liters): "))

    try:
        # Convert date string to date object
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # Create and save WaterIntake instance
        water_intake = WaterIntake(user_id=user_id, date=date_obj, amount=amount)
        water_intake.save()
        print("Water intake logged successfully.")

    except ValueError as e:
        print(f"Error: {e}")

def view_water_intake():
    try:
        with get_session() as session:
            water_intakes = session.query(WaterIntake).all()
            if water_intakes:
                for water in water_intakes:
                    print(f"ID: {water.id}, User ID: {water.user_id}, Date: {water.date}, Amount: {water.amount} liters")
            else:
                print("No water intake records found.")
    except SQLAlchemyError as e:
        print(f"Error viewing water intake: {e}")

def generate_report():
    from report import Report
    try:
        user_id = input("Enter user ID for report: ").strip()
        if not user_id.isdigit():
            print("Invalid ID. Please enter a numeric value.")
            return

        user_id = int(user_id)
        
        # Using a session context manager
        with get_session() as session:
            report = Report(user_id=user_id)
            # Generate report data
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
            print("Exiting the application.")
            break
        else:
            print("Invalid choice. Please select a valid option.")


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
            print("Invalid choice. Please select a valid option.")


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
            print("Invalid choice. Please select a valid option.")


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
            print("Invalid choice. Please select a valid option.")


# Run the Application
if __name__ == "__main__":
    main_menu()
