from datetime import datetime
from sqlalchemy import (create_engine, Column, Integer, String, Float,
                        TIMESTAMP, ForeignKey)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Mapped, mapped_column

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    registered_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class Stats(Base):
    __tablename__ = "stats"

    id = Column(Integer, primary_key=True)
    wid = Column(Integer, ForeignKey("workouts.id"))
    record_weight = Column(Integer)
    workout = relationship("Workout", back_populates="stats")
