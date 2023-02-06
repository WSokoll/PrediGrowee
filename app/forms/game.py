from flask_wtf import FlaskForm
from wtforms import RadioField
from wtforms.validators import InputRequired

DIRECTION_CHOICES = [(1, 'predominantly horizontal'), (2, 'predominantly vertical'), (3, 'mixed')]


class GameForm(FlaskForm):
    direction = RadioField('Direction of the facial growth', choices=DIRECTION_CHOICES, validators=[InputRequired()])
