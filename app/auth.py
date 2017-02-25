from flask import jsonify
from flask.helpers import make_response
from flask_httpauth import HTTPBasicAuth

from .models import Account

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    account = Account.query.filter_by(username=username).first()
    return account and account.auth_id == password


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)
