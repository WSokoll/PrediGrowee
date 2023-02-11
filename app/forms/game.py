from flask_wtf import FlaskForm
from wtforms import RadioField, HiddenField
from wtforms.validators import InputRequired

DIRECTION_CHOICES = [(0, 'predominantly horizontal'), (1, 'predominantly vertical'), (2, 'mixed')]


class GameForm(FlaskForm):
    direction = RadioField('Direction of the facial growth', choices=DIRECTION_CHOICES, validators=[InputRequired()])
    screen_size = HiddenField('Screen size')  # TODO validators
    show_results = HiddenField('Show results')  # TODO validators
