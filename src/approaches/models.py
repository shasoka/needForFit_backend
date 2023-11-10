from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base


class Approach(Base):
    __tablename__ = "approaches"

    id: Mapped[int] = mapped_column(primary_key=True)
    eid: Mapped[int] = mapped_column(ForeignKey("exercises.id"))
    wid: Mapped[int] = mapped_column(ForeignKey("workouts.id"))
    reps: Mapped[int] = mapped_column()
    weight: Mapped[int] = mapped_column()
    time: Mapped[float] = mapped_column()
