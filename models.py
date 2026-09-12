from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base

# Habit Table
class Habit(Base):
    __tablename__ = "habits"

    # Habit has id, name, and creation time
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    completions = relationship("Completion", back_populates="habit", cascade="all, delete-orphan")


# Completion Table
class Completion(Base):
    __tablename__ = "completions"

    # Completed Habits have id, habit_id, and completed date
    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, ForeignKey("habits.id"), nullable=False)
    completed_date = Column(Date, nullable=False)

    habit = relationship("Habit", back_populates="completions")