from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey, JSON
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.models import Base


class Exercise(Base):
    __tablename__ = "exercises"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    image: Mapped[str] = mapped_column(nullable=False)

    approaches: Mapped[List["Approach"]] = relationship("Approach", back_populates="exercise")


class Workout(Base):
    __tablename__ = "workouts"

    id: Mapped[int] = mapped_column(primary_key=True)
    uid: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    approaches: Mapped[List["Approach"]] = relationship("Approach", back_populates="workout")
    user: Mapped["User"] = relationship("User", back_populates="workouts")
    stat: Mapped["LocalStats"] = relationship("LocalStats", back_populates="workout")


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
    username: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    registered_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

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
    wid: Mapped[int] = mapped_column(ForeignKey("workouts.id"))
    exercises_count: Mapped[int] = mapped_column(nullable=True)
    max_weights: Mapped[dict] = mapped_column(JSON, nullable=True)
    max_reps: Mapped[dict] = mapped_column(JSON, nullable=True)
    favorite_exercise: Mapped[str] = mapped_column(nullable=True)
    total_weight: Mapped[int] = mapped_column(nullable=True)

    workout: Mapped["Workout"] = relationship("Workout", back_populates="stat")
