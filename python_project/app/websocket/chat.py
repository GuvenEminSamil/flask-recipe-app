from flask import Blueprint, render_template, session
from flask_socketio import emit
from app import socketio, db
from app.models import Message

socketio_bp = Blueprint("socket", __name__)

@socketio_bp.route("/chat")
def chat():
    username = session.get("username", "Guest")
    messages = Message.query.order_by(Message.timestamp.asc()).limit(100).all()
    return render_template("chat.html", username=username, messages=messages)

@socketio.on("message")
def handle_message(msg):
    username = session.get("username", "Guest")

    message = Message(username=username, content=msg)
    db.session.add(message)
    db.session.commit()

    emit("message", f"{username}: {msg}", broadcast=True)