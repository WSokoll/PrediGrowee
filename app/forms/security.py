from flask_security import RegisterForm, LoginForm
from flask_wtf import RecaptchaField


class ExtendedRegisterForm(RegisterForm):
    recaptcha = RecaptchaField()


class CustomLoginForm(LoginForm):
    def validate(self):
        response = super(CustomLoginForm, self).validate()

        if self.user and self.user.password is None and self.user.register_only_google:
            self.form_errors.append('You have logged in with Google account before. '
                                    'If you want to use this form of logging in, you must first log in using Google,'
                                    ' and then set a password using the "Set password" button.')
            self.password.errors.clear()

        # User has set a password and can log in using email and password form - update register_only_google field
        elif self.user and self.user.password and self.user.register_only_google:
            self.user.register_only_google = False

        return response
