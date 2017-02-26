import datetime
import logging

from flask.globals import request
from flask_restful import Resource

from app import api, redis_store, app
from app.auth import auth
from app.error_handler import error_handler
from app.models import PhoneNumber, Account
from app.parsers import get_parser, abort

logger = logging.getLogger(__name__)


def get_redis_key(domain, *args, sep="~"):
    return "~".join(list(args)+[domain])


class InboundSMSAPI(Resource):

    decorators = [auth.login_required, error_handler]

    def post(self):
        parser = get_parser()
        data = parser.parse_args(request)
        phone_number = PhoneNumber.query.filter_by(number=data.get("to")).first()
        if not phone_number:
            abort(400, error="to parameter not found")
        text = data.get("text").rstrip("\r\n").rstrip("\r").rstrip("\n")
        if text == "STOP":
            logger.info("Stopping with number ", data.get("from"), " and ", data.get("to"))
            redis_store.set(get_redis_key("STOP", data.get("from"), data.get("to")), True, ex=4*60*60)
        return {"message": "inbound sms ok", "error": ""}


class OutboundSMSAPI(Resource):
    decorators = [auth.login_required, error_handler]

    @staticmethod
    def validate_stop(from_number, to_number):
        if redis_store.get(get_redis_key("STOP", from_number, to_number)):
            abort(400, message="", error="sms from {0} to {1} blocked by STOP request".format(from_number, to_number))

    @staticmethod
    def validate_from_throttle(from_number):
        seconds = app.config['SMS_THROTTLE_SECONDS']
        max_count = app.config['SMS_THROTTLE_MAX_COUNT']
        key = get_redis_key("FROM_THROTTLE", from_number)
        existing_obj = redis_store.get(key)
        current_timestamp = datetime.datetime.now()
        if not existing_obj:
            redis_store.set(key, "{0}~{1}".format(1, current_timestamp.timestamp()), ex=seconds)
            return
        count, timestamp = existing_obj.decode().split("~")
        first_timestamp = datetime.datetime.fromtimestamp(float(timestamp))
        count = int(count)
        if count >= max_count:
            abort(400, error="limit reached for from {0}".format(from_number))
        else:
            count += 1
            expires_in = (first_timestamp + datetime.timedelta(seconds=seconds)) - current_timestamp
            redis_store.set(key, "{0}~{1}".format(count, timestamp), ex=expires_in)

    def post(self):
        parser = get_parser()
        data = parser.parse_args(request)
        from_number = data.get("from")
        to_number = data.get("to")

        self.validate_stop(from_number, to_number)
        account = Account.query.filter_by(username=auth.username()).first()
        validated_phone_number = PhoneNumber.query.filter_by(number=from_number, account_id=account.id).first()
        if not validated_phone_number:
            abort(400, error="from parameter not found")
        self.validate_from_throttle(from_number)

        return {"message": "outbound sms ok", "error": ""}


api.add_resource(InboundSMSAPI, '/inbound/sms')
api.add_resource(OutboundSMSAPI, '/outbound/sms')
