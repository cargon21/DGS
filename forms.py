# This forms.py file contains the class structure for the website forms. Here wtforms is used
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, DateField, DecimalField, IntegerField, TextAreaField, SubmitField, MultipleFileField, PasswordField
from wtforms.validators import DataRequired, Length, NumberRange, InputRequired

# Form for logging in to the admin page
class Login(FlaskForm):
    username = StringField('Username', validators = [DataRequired(), Length(max = 25)])
    password = PasswordField('Passowrd', validators=[DataRequired(), Length(max=25)])
    submit = SubmitField('Submit')

# Form for adding a game to DB
class AddGame(FlaskForm):
    title = StringField('Game Title', validators = [DataRequired(), Length(max = 40)])
    developer = StringField('Developer', validators=[DataRequired(), Length(max=40)])
    publisher = StringField('Publisher', validators=[DataRequired(), Length(max=40)])
    genre = StringField('Genre', validators=[DataRequired(), Length(max=25)])
    releaseDate = DateField('Release Date', render_kw={"placeholder": "mm-dd-yyyy"}, format='%m-%d-%Y', validators=[DataRequired()])
    price = DecimalField('Price $', render_kw={"placeholder": "ex. 19.99"}, validators= [InputRequired()])
    rating = IntegerField('Rating %', validators=[InputRequired(), NumberRange(0,100)])
    siteName = StringField('Website Name', validators=[DataRequired(), Length(max=25)])
    siteURL= StringField('Website URL', validators=[DataRequired(), Length(max=125)])
    imageURL = FileField('Image', validators=[FileAllowed(['jpg', 'png', 'JPEG'])])
    description = TextAreaField('Game Description', validators=[DataRequired(), Length(max=250)])
    submit = SubmitField('Submit')

# Form for adding a price to DB
class AddPrice(FlaskForm):
    title = StringField('Game Title', validators = [DataRequired(), Length(max = 40)])
    price = DecimalField('Price', render_kw={"placeholder": "ex. 19.99"}, validators= [InputRequired()])
    siteName = StringField('Website Name', validators=[DataRequired(), Length(max=25)])
    siteURL= StringField('Website URL', validators=[DataRequired(), Length(max=125)])
    submit = SubmitField('Submit')

# Form for deleting a game from DB
class DeleteGame(FlaskForm):
    title = StringField('Game Title', validators = [DataRequired(), Length(max = 40)])
    submit = SubmitField('Submit')

# Form for deleting a price from DB
class DeletePrice(FlaskForm):
    title = StringField('Game Title', validators = [DataRequired(), Length(max = 40)])
    price = DecimalField('Price', render_kw={"placeholder": "ex. 19.99"}, validators= [InputRequired()])
    submit = SubmitField('Submit')