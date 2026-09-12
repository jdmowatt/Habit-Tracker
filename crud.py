from sqlalchemy.orm import Session
from datetime import date, timedelta
import models
import schemas

# Create a Habit
def create_habit(db: Session, habit: schemas.HabitCreate) -> models.Habit:
    db_habit = models.Habit(name=habit.name)
    db.add (db_habit)
    db.commit()
    db.refresh(db_habit)
    return db_habit

# Get all Habits
def get_habits(db: Session) -> list[models.Habit]:
    return db.query(models.Habit).all()

# Get a Habit
def get_habit(db: Session, habit_id: int) -> models.Habit | None:
    return db.query(models.Habit).filter(models.Habit.id == habit_id).first()

# Delete a Habit
def delete_habit(db: Session, habit_id: int) -> bool:
    db_habit = get_habit(db, habit_id)
    if db_habit is None:
        return False
    db.delete(db_habit)
    db.commit()
    return True

# Create a Completed Habit
def create_completion(db: Session, habit_id: int, completed_date: date | None) -> models.Completion:
    if completed_date is None:
        completed_date = date.today()
    db_completion = models.Completion(habit_id=habit_id, completed_date=completed_date)
    db.add (db_completion)
    db.commit()
    db.refresh(db_completion)
    return db_completion

# Return all Completed Habits
def get_completions(db: Session, habit_id: int) -> list[models.Completion]:
    return db.query(models.Completion).filter(models.Completion.habit_id == habit_id).all()

# Return Streak of Habit
def get_streak(db: Session, habit_id: int) -> int:
    completions = get_completions(db, habit_id)
    completed_dates = {c.completed_date for c in completions}

    today = date.today()

    if today in completed_dates:
        current = today
    elif today - timedelta(days=1) in completed_dates:
        current = today - timedelta(days=1)
    else:
        return 0

    streak = 0
    while current in completed_dates:
        streak += 1
        current = current - timedelta(days=1)

    return streak