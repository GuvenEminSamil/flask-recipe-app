from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField
from wtforms.validators import DataRequired, Length, Email

class FeedbackForm(FlaskForm):
    user_email = StringField("User Email", validators=[DataRequired(), Email()])
    title = TextAreaField(validators=[DataRequired(), Length(max=80)])
    feedback = TextAreaField(validators=[DataRequired(), Length(max=2000)])
    submit = SubmitField("Send Feedback")