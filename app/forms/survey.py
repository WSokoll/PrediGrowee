from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, StringField
from wtforms.validators import InputRequired, Length

from app.validators import AgeValidator, OtherEducationValidator

VISION_DEFECT_CHOICES = [
    'I do not have any vision defects.',
    'I use correction glasses.',
    'I should use correction glasses but I do not use them now.'
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


class SurveyForm(FlaskForm):
    gender = SelectField('Gender', choices=['male', 'female'], validators=[InputRequired()])
    age = IntegerField('Age', validators=[InputRequired(), AgeValidator(18, 130)])
    vision_defect = SelectField('Vision defect', choices=VISION_DEFECT_CHOICES, validators=[InputRequired()])
    education = SelectField('Education', choices=EDUCATION_CHOICES, validators=[InputRequired()])
    education_other = StringField('Education', validators=[Length(max=255), OtherEducationValidator()])
    experience = SelectField('Experience with cephalometric analysis',
                             choices=EXPERIENCE_CHOICES,
                             validators=[InputRequired()])

