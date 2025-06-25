from app import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey
from typing import List, Optional


class Recipe(db.Model):
    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(String(100), nullable=False)
    category : Mapped[str] = mapped_column(String(100))
    area : Mapped[str] = mapped_column(String(100))
    instructions : Mapped[str] = mapped_column(Text)
    thumbnail : Mapped[Optional[str]] = mapped_column(nullable=True)
    comments : Mapped[List["Comment"]] = relationship("Comment", backref="recipe", cascade="all, delete")
    user_id : Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"))
    author : Mapped[Optional["User"]] = relationship("User", back_populates="recipes")


    def __repr__(self):
        return f"<Recipe {self.name}"