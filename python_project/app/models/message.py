from app import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Text, DateTime
from datetime import datetime

class Message(db.Model):
    id : Mapped[int] = mapped_column(primary_key=True)
    username : Mapped[str] = mapped_column(String(80), nullable=False)
    content : Mapped[str] = mapped_column(Text, nullable=False)
    timestamp : Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)