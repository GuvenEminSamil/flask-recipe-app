from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField

class PreferencesForm(FlaskForm):
    dark_mode = BooleanField("Enable Dark Mode")
    submit = SubmitField("Save Preferences")
