from flask_wtf import FlaskForm
from wtforms import RadioField, HiddenField
from wtforms.validators import InputRequired, Regexp

# The first value of the tuple should indicate position on the list
DIRECTION_CHOICES = [(0, 'predominantly horizontal'), (1, 'predominantly vertical'), (2, 'mixed')]


class GameForm(FlaskForm):
    direction = RadioField('Direction of the facial growth', choices=DIRECTION_CHOICES, validators=[InputRequired()])
    screen_size = HiddenField('Screen size')  # <-- validation done after form submission
    show_results = HiddenField('Show results', validators=[
        InputRequired('Please use dedicated buttons to submit the prediction form.'),
        Regexp(r'^true$|^false$', message='Please use dedicated buttons to submit the prediction form.')
    ])
