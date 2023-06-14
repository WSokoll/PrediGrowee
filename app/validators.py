from wtforms import ValidationError


class AgeValidator:
    """Validator for IntegerField. Validates that given number (age) is between min_age and max_age.

    :param min_age: minimal age
    :param max_age: maximal age
    :param message: error message
    """

    def __init__(self, min_age, max_age, message=None):
        self.min_age = min_age
        self.max_age = max_age
        self.message = message

    def __call__(self, form, field):

        if field.data < self.min_age:
            raise ValidationError(
                self.message or
                field.gettext('You must be at least {min_age} years old to use the app.'.format(min_age=self.min_age))
            )

        elif field.data > self.max_age:
            raise ValidationError(
                self.message or
                field.gettext('An invalid number has been entered.')
            )


class OtherEducationValidator:
    """If the 'other' option has been selected in the education field, then the education_other field is required

     :param message: error message
    """

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):

        if form.education.data == 'other' and not field.data:
            raise ValidationError(
                self.message or
                field.gettext('Please fill in the education field.')
            )


class IncludedValidator:
    """If the 'yes' option has been selected in the included field, then the name and surname fields are required

     :param message: error message
    """

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):

        if form.included.data == 'Yes' and not field.data:
            raise ValidationError(
                self.message or
                field.gettext(f'Please fill in the {field.name} field.')
            )
