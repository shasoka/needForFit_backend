from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey, JSON
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.models import Base
from src.config import SERVER_HOST, SERVER_PORT


class Exercise(Base):
    __tablename__ = "exercises"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    image: Mapped[str] = mapped_column(nullable=False)
    image_url: Mapped[str] = mapped_column()
    video_url: Mapped[str] = mapped_column()
    tid: Mapped[int] = mapped_column(ForeignKey("exercise_types.id"))

    approaches: Mapped[List["Approach"]] = relationship("Approach", back_populates="exercise")
    exercise_type: Mapped["ExerciseTypes"] = relationship("ExerciseTypes", back_populates="exercises")


class ExerciseTypes(Base):
    __tablename__ = "exercise_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    exercises: Mapped[List["Exercise"]] = relationship("Exercise", back_populates="exercise_type")


class Workout(Base):
    __tablename__ = "workouts"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, default="New workout")
    uid: Mapped[int] = mapped_column(ForeignKey("users.id"))
    tid: Mapped[int] = mapped_column(ForeignKey("workout_types.id"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    approaches: Mapped[List["Approach"]] = relationship("Approach", back_populates="workout")
    user: Mapped["User"] = relationship("User", back_populates="workouts")
    stat: Mapped["LocalStats"] = relationship("LocalStats", back_populates="workout")
    workout_type: Mapped["WorkoutTypes"] = relationship("WorkoutTypes", back_populates="workouts")


class WorkoutTypes(Base):
    __tablename__ = "workout_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    uid: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship("User", back_populates="workout_types")
    workouts: Mapped[List["Workout"]] = relationship("Workout", back_populates="workout_type")


class DayPhrase(Base):
    __tablename__ = "day_phrase"

    id: Mapped[int] = mapped_column(primary_key=True)
    phrase: Mapped[str] = mapped_column(nullable=False)
    uid: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True, unique=True)

    user: Mapped["User"] = relationship("User", back_populates="day_phrase")


class Approach(Base):
    __tablename__ = "approaches"

    id: Mapped[int] = mapped_column(primary_key=True)
    eid: Mapped[int] = mapped_column(ForeignKey("exercises.id"))
    wid: Mapped[int] = mapped_column(ForeignKey("workouts.id"))
    reps: Mapped[int] = mapped_column()
    weight: Mapped[int] = mapped_column()
    time: Mapped[float] = mapped_column()

    exercise: Mapped["Exercise"] = relationship("Exercise", back_populates="approaches")
    workout: Mapped[Workout] = relationship("Workout", back_populates="approaches")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    profile_picture: Mapped[str] = mapped_column(
        nullable=False,
        default=SERVER_HOST+":"+SERVER_PORT+"/static/images/users/profile_picture_placeholder.png")
    registered_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    workout_types: Mapped[List["WorkoutTypes"]] = relationship("WorkoutTypes", back_populates="user")
    day_phrase: Mapped[List["DayPhrase"]] = relationship("DayPhrase", back_populates="user")
    workouts: Mapped[List["Workout"]] = relationship("Workout", back_populates="user")
    stat: Mapped["GlobalStats"] = relationship("GlobalStats", back_populates="user")


class GlobalStats(Base):
    __tablename__ = "global_stats"

    id: Mapped[int] = mapped_column(primary_key=True)
    uid: Mapped[int] = mapped_column(ForeignKey("users.id"))
    ttl_weight: Mapped[int] = mapped_column(nullable=True)
    ttl_reps: Mapped[int] = mapped_column(nullable=True)
    max_weight: Mapped[int] = mapped_column(nullable=True)
    ttl_workouts: Mapped[int] = mapped_column(nullable=True)

    user: Mapped[User] = relationship("User", back_populates="stat")


class LocalStats(Base):
    __tablename__ = "local_stats"

    id: Mapped[int] = mapped_column(primary_key=True)
    wid: Mapped[int] = mapped_column(ForeignKey("workouts.id"), unique=True)
    exercises_count: Mapped[int] = mapped_column(nullable=True)
    max_weights: Mapped[dict] = mapped_column(JSON, nullable=True)
    max_reps: Mapped[dict] = mapped_column(JSON, nullable=True)
    favorite_exercise: Mapped[str] = mapped_column(nullable=True)
    total_weight: Mapped[int] = mapped_column(nullable=True)

    workout: Mapped["Workout"] = relationship("Workout", back_populates="stat")
