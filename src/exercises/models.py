from typing import List

from sqlalchemy.orm import mapped_column, Mapped, relationship

from workouts.models import Approach
from src.models import Base


class Exercise(Base):
    __tablename__ = "exercises"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    image: Mapped[str] = mapped_column(nullable=False)

    children: Mapped[List[Approach]] = relationship()
