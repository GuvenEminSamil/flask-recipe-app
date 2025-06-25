from app import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text
from typing import List


class Recipe(db.Model):
    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(String(100), nullable=False)
    category : Mapped[str] = mapped_column(String(100))
    area : Mapped[str] = mapped_column(String(100))
    instructions : Mapped[str] = mapped_column(Text)
    thumbnail : Mapped[str] = mapped_column(String(100))
    comments : Mapped[List["Comment"]] = relationship("Comment", backref="recipe", cascade="all, delete")


    def __repr__(self):
        return f"<Recipe {self.name}"