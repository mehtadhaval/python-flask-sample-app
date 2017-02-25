# config.py

# Enable Flask's debugging features. Should be False in production
DEBUG = False
SQLALCHEMY_DATABASE_URI = "postgresql://postgres:nopasswordset@localhost/sample_app"
SQLALCHEMY_TRACK_MODIFICATIONS = False
REDIS_URL = "redis://user:password@localhost:6379/0"

# App specific settings
SMS_THROTTLE_SECONDS = 24*60*60
SMS_THROTTLE_MAX_COUNT = 50