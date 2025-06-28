from flask.views import MethodView
from flask import render_template, redirect, url_for, session
from app.models import Feedback, User


class AdminFeedbackView(MethodView):
    def get(self):
        user = User.query.get(session.get("user_id"))

        if not user or not user.role:
            return redirect(url_for("main"))

        feedbacks = Feedback.query.all()
        return render_template("admin/feedbacks.html", feedbacks=feedbacks, User=user, user=user)