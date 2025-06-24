from app import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer


class User(db.Model):
    id : Mapped[int] = mapped_column(primary_key=True)
    username : Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    email : Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    password_hash : Mapped[str] = mapped_column(String(5000), nullable=False)


    def __repr__(self):
        return f"<User {self.username}>"

