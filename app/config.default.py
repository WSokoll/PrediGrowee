# Do not change the values below!
# If a change is required copy appropriate lines to the /local/config.local.py file and change the values there.

SECRET_KEY = 'please_change_@187%0^&'

# Dict of columns shown in the game
ORT_DATA_COLUMNS = {
    'sn_mp': 'SN/MP',
    'facial_axis': 'Facial Axis',
    'y_axis': 'Y-Axis',
    'point_a_to_nasion_perp': 'Point A to Nasion Perp',
    'pog_to_nasion_perp': 'Pog to Nasion Perp',
    'antegonial_notch_depth': 'Antegonial Notch Depth',
    'mn_base_angle': 'Mn Base Angle',
    'mn_ramus_angle': 'Mn Ramus Angle',
    'sn_pog': 'SNPog',
    'snb': 'SNB',
    'sna': 'SNA',
    'sn_pp': 'SN/PP',
    'anb': 'ANB',
    'afh_pfh': 'AFH:PFH',
    'point_a_to_pog_along_fh': 'Point A to Pog along FH'
}

# Absolute path to 'orto' folder containing photos
ORT_FOLDER_PATH = 'C:/example/path'

# Database connection
DB_HOST = 'localhost'
DB_PORT = 3306
DB_NAME = 'test'
DB_USER = 'test'
DB_PASSWORD = 'test'

# Recaptcha (can be generated via https://www.google.com/recaptcha/admin/create)
RECAPTCHA_PUBLIC_KEY = 'recaptcha_public_key'
RECAPTCHA_PRIVATE_KEY = 'recaptcha_private_key'
RECAPTCHA_VERIFY_SERVER = 'https://www.google.com/recaptcha/api/siteverify'

# OAuth
GOOGLE_CLIENT_ID = 'google_client_id'
GOOGLE_CLIENT_SECRET = 'google_client_secret'
GOOGLE_CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'

# Mail config
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USERNAME = 'no-reply@localhost'
MAIL_PASSWORD = 'test'
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_DEFAULT_SENDER = 'no-reply@localhost'

# Security
SECURITY_PASSWORD_SALT = '9873313545127551081313677346265396239529'

SECURITY_FLASH_MESSAGES = True
SECURITY_PASSWORD_LENGTH_MIN = 8

SECURITY_POST_LOGIN_VIEW = '/'
SECURITY_POST_LOGOUT_VIEW = '/'

SECURITY_REGISTERABLE = True
SECURITY_SEND_REGISTER_EMAIL = True
SECURITY_EMAIL_SUBJECT_REGISTER = 'PrediGrowee - Account registration'
SECURITY_POST_REGISTER_VIEW = 'security.login'
SECURITY_USERNAME_ENABLE = False
SECURITY_USERNAME_REQUIRED = False

SECURITY_CONFIRMABLE = True
SECURITY_CONFIRM_EMAIL_WITHIN = '2 days'
SECURITY_CONFIRM_URL = '/confirm'
SECURITY_EMAIL_SUBJECT_CONFIRM = 'PrediGrowee - Email confirmation'
SECURITY_POST_CONFIRM_VIEW = 'security.login'
SECURITY_AUTO_LOGIN_AFTER_CONFIRM = False
SECURITY_LOGIN_WITHOUT_CONFIRMATION = False

SECURITY_CHANGEABLE = True
SECURITY_POST_CHANGE_VIEW = '/'
SECURITY_SEND_PASSWORD_CHANGE_EMAIL = True
SECURITY_EMAIL_SUBJECT_PASSWORD_CHANGE_NOTICE = 'PrediGrowee - Your password has been changed'

SECURITY_RECOVERABLE = False
SECURITY_TWO_FACTOR = False
SECURITY_TWO_FACTOR_REQUIRED = False
SECURITY_UNIFIED_SIGNIN = False
SECURITY_PASSWORDLESS = False
SECURITY_TRACKABLE = True
SECURITY_WEBAUTHN = False
SECURITY_MULTI_FACTOR_RECOVERY_CODES = False
