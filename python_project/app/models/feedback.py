from app import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, ForeignKey

class Feedback(db.Model):
    id : Mapped[int] = mapped_column(primary_key=True)
    user_email : Mapped[str] = mapped_column(nullable=False)
    title : Mapped[str] = mapped_column(String(80), nullable=False)
    feedback : Mapped[str] = mapped_column(Text, nullable=False)
