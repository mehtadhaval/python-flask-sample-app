import logging

from flask.globals import request
from flask_restful import Resource

from app import api, redis_store
from app.auth import auth
from app.models import PhoneNumber
from app.parsers import get_inbound_parser, abort

logger = logging.getLogger(__name__)


class InboundSMSAPI(Resource):

    decorators = [auth.login_required]

    def post(self):
        parser = get_inbound_parser()
        data = parser.parse_args(request)
        phone_number = PhoneNumber.query.filter_by(number=data.get("to")).first()
        if not phone_number:
            abort(400, error="to parameter not found")
        text = data.get("text").rstrip("\r\n").rstrip("\r").rstrip("\n")
        if text == "STOP":
            logger.info("Stopping with number ", data.get("from"), " and ", data.get("to"))
            redis_store.set("{from}~{to}".format(**data), True, ex=4*60*60)
        return {"message": "inbound sms ok", "error": ""}


class OutboundSMSAPI(Resource):
    decorators = [auth.login_required]

    def post(self):
        return {}

api.add_resource(InboundSMSAPI, '/inbound/sms')
api.add_resource(OutboundSMSAPI, '/outbound/sms')
