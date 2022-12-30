from flask_security import RegisterForm
from flask_wtf import RecaptchaField


class ExtendedRegisterForm(RegisterForm):
    recaptcha = RecaptchaField()
