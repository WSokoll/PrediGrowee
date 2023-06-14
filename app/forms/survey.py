from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, StringField, RadioField
from wtforms.validators import InputRequired, Length
import pycountry

from app.validators import AgeValidator, OtherEducationValidator, IncludedValidator

VISION_DEFECT_CHOICES = [
    'I do not have any vision defects.',
    'I use correction glasses or contact lenses.',
    'I should use correction glasses or contact lenses, but I do not use them now.'
]

EDUCATION_CHOICES = [
    'dental student',
    'dental graduate ',
    'general dental practitioner',
    'postgraduate orthodontic student',
    'ortodontic specialist',
    'other'
]

EXPERIENCE_CHOICES = [
    'less than 1 year',
    '1-3 years',
    '3-7 years',
    '7-10 years',
    'more than 10 years'
]


class CountrySelectField(SelectField):
    def __init__(self, *args, **kwargs):
        super(CountrySelectField, self).__init__(*args, **kwargs)
        countries = sorted([c.name for c in pycountry.countries])
        self.choices = [(country, country) for country in countries]


class SurveyForm(FlaskForm):
    gender = SelectField('Gender', choices=['Male', 'Female', 'Prefer not to say'], validators=[InputRequired()])
    age = IntegerField('Age', validators=[InputRequired(), AgeValidator(18, 130)])
    country = CountrySelectField('Country of origin', default="Poland", validators=[InputRequired()])
    vision_defect = SelectField('Vision defect', choices=VISION_DEFECT_CHOICES, validators=[InputRequired()])
    education = SelectField('Education', choices=EDUCATION_CHOICES, validators=[InputRequired()])
    education_other = StringField('Education', validators=[Length(max=255), OtherEducationValidator()])
    experience = SelectField('Experience with cephalometric analysis',
                             choices=EXPERIENCE_CHOICES,
                             validators=[InputRequired()])
    included = RadioField('Would you like to be included in acknowledgements of our future papers?',
                          choices=[('Yes', 'Yes'), ('No', 'No')],
                          validators=[InputRequired()])
    name = StringField('Name', validators=[Length(max=100), IncludedValidator()])
    surname = StringField('Surname', validators=[Length(max=100), IncludedValidator()])
