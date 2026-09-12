from pydantic import BaseModel, ConfigDict
from datetime import datetime, date
from typing import List

# Create Habit
class HabitCreate(BaseModel):
    name: str

# Return Habit
class Habit(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    created_at: datetime

# Create Completion
class CompletionCreate(BaseModel):
    completed_date: date | None = None

# Return Completion
class Completion(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    habit_id: int
    completed_date: date