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
