from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed, FileField, FileRequired

class RecipeForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    category = StringField("Category", validators=[DataRequired()])
    area = StringField("Area", validators=[DataRequired()])
    instructions = TextAreaField("Instructions", validators=[DataRequired()])
    image = FileField("Upload Image", validators=[FileAllowed(["jpg", "jpeg", "png", "gif"]),
                                                  FileRequired(message="Image is required")])
    submit = SubmitField("Submit")
