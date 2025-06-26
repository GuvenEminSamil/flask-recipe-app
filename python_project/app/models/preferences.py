from app import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Boolean

class UserPreferences(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    dark_mode: Mapped[bool] = mapped_column(default=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), unique=True)
    user = relationship("User", back_populates="preferences", uselist=False)
