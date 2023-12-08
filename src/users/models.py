from datetime import datetime
from typing import List

from sqlalchemy import (create_engine, Column, Integer, String, Float,
                        TIMESTAMP, ForeignKey)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Mapped, mapped_column

from workouts.models import Workout

from models import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    registered_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    children_w: Mapped[List["Workout"]] = relationship()
    children_s: Mapped["GlobalStats"] = relationship()


class GlobalStats(Base):
    __tablename__ = "global_stats"

    id: Mapped[int] = mapped_column(primary_key=True)
    ttl_weight: Mapped[int] = mapped_column(nullable=True)
    ttl_reps: Mapped[int] = mapped_column(nullable=True)
    ttl_time: Mapped[float] = mapped_column(nullable=True)
    max_weight: Mapped[int] = mapped_column(nullable=True)
    uid: Mapped[int] = mapped_column(ForeignKey("users.id"))
