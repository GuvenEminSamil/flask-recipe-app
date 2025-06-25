from app import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean
from app.models.recipe import Recipe
from app.models.favorite import favorite_table
from typing import List


class User(db.Model):
    id : Mapped[int] = mapped_column(primary_key=True)
    username : Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    email : Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    password_hash : Mapped[str] = mapped_column(String(5000), nullable=False)
    oauth_provider = mapped_column(String(20), nullable=True)
    favorites = db.relationship("Recipe", secondary=favorite_table, backref="liked_by")
    comments: Mapped[List["Comment"]] = relationship("Comment", backref="user", cascade="all, delete")

    def __repr__(self):
        return f"<User {self.username}>"

