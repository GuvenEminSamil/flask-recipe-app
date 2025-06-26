from app import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

class ContactUs(db.Model):
    id : Mapped[int] = mapped_column(primary_key=True)
    content : Mapped[str] = mapped_column(String(200))