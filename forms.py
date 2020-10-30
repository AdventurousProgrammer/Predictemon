from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class PokemonSubmissionForm(FlaskForm):
    pokemon1 = StringField('pokemon1',
            validators=[DataRequired(), Length(min=2, max=20)])
    pokemon2 = StringField('pokemon2',
                           validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Battle!')

class LoginForm(FlaskForm):
    username = StringField('username',
            validators=[DataRequired(), Length(min=2, max=20)])
    password = StringField('password',
                           validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Log In')