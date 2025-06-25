from app import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, ForeignKey, Text
from datetime import datetime

class Comment(db.Model):
    id : Mapped[int] = mapped_column(primary_key=True)
    content : Mapped[str] = mapped_column(Text, nullable=False)
    created_at : Mapped[datetime] = mapped_column(default=datetime.utcnow)

    user_id : Mapped[int] = mapped_column(ForeignKey("user.id"),nullable=False)
    recipe_id : Mapped[int] = mapped_column(ForeignKey("recipe.id"), nullable=False)