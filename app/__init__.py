# app/__init__.py

from flask import Flask

# Initialize the app
from flask_redis import FlaskRedis
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)

# Load the config file
app.config.from_object('config')
try:
    app.config.from_object('config_dev')
except ImportError:
    pass
db = SQLAlchemy(app)
api = Api(app)
redis_store = FlaskRedis(app)

# Load the views
from app import views, models
