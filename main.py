from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import engine, Base, SessionLocal
import models
import schemas
import crud

# Sync Python Class Tables with Database Tables
Base.metadata.create_all(bind=engine)

# Create App
app = FastAPI()

# Access Database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/habits", response_model=schemas.Habit)
def create_habit(habit: schemas.HabitCreate, db: Session = Depends(get_db)):
    return crud.create_habit(db, habit)

@app.get("/habits", response_model=list[schemas.Habit])
def list_habits(db: Session = Depends(get_db)):
    return crud.get_habits(db)

@app.get("/habits/{habit_id}", response_model=schemas.Habit)
def get_habit(habit_id: int, db: Session = Depends(get_db)):
    db_habit = crud.get_habit(db, habit_id)
    if db_habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")
    return db_habit

@app.delete("/habits/{habit_id}")
def delete_habit(habit_id: int, db: Session = Depends(get_db)):
    success = crud.delete_habit(db, habit_id)
    if not success:
        raise HTTPException(status_code=404, detail="Habit not found")
    return {"message": "Habit deleted"}

@app.post("/habits/{habit_id}/complete", response_model=schemas.Completion)
def complete_habit(habit_id: int, completion: schemas.CompletionCreate, db: Session = Depends(get_db)):
    db_habit = crud.get_habit(db, habit_id)
    if db_habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")
    return crud.create_completion(db, habit_id, completion.completed_date)

@app.get("/habits/{habit_id}/completions", response_model=list[schemas.Completion])
def list_completions(habit_id: int, db: Session = Depends(get_db)):
    db_habit = crud.get_habit(db, habit_id)
    if db_habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")
    return crud.get_completions(db, habit_id)

@app.get("/habits/{habit_id}/streak")
def get_streak(habit_id: int, db: Session = Depends(get_db)):
    db_habit = crud.get_habit(db, habit_id)
    if db_habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")
    streak = crud.get_streak(db, habit_id)
    return {"habit_id": habit_id, "streak": streak}