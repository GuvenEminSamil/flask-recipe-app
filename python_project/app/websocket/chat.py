from flask import Blueprint, render_template, session
from flask_socketio import emit
from app import socketio, db
from app.models import Message, User

socketio_bp = Blueprint("socket", __name__)

@socketio_bp.route("/chat")
def chat():
    username = session.get("username", "Guest")
    messages = Message.query.order_by(Message.timestamp.asc()).limit(100).all()
    user = User.query.get(session.get("user_id"))
    return render_template("chat.html", username=username, messages=messages, User=user, user=user)

@socketio.on("message")
def handle_message(msg):
    username = session.get("username", "Guest")

    message = Message(username=username, content=msg)
    db.session.add(message)
    db.session.commit()

    emit("message", f"{username}: {msg}", broadcast=True)