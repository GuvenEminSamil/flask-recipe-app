from flask import render_template, session, flash, redirect, url_for
from flask.views import MethodView
from app import db
from app.models.feedback import Feedback
from app.forms.feedback_form import FeedbackForm

class FeedbackCreateView(MethodView):
    def post(self):
        if "user_id" not in session:
            flash("You must be logged in to create a feedback", "danger")
            return redirect(url_for("login"))

        form = FeedbackForm()
        if form.validate_on_submit():
            feedback = Feedback(
                user_email=form.user_email.data,
                title=form.title.data,
                feedback=form.feedback.data
            )
            db.session.add(feedback)
            db.session.commit()
            flash("Your feedback has been submitted", "success")

        return redirect(url_for("home", form=form))

    def get(self):
        if "user_id" not in session:
            flash("You must be logged in to create a feedback", "danger")
            return redirect(url_for("login"))

        return render_template("feedback.html", form=FeedbackForm())