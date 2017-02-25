from flask_restful import Resource

from app import api
from app.auth import auth


class InboundSMSAPI(Resource):
    decorators = [auth.login_required]

    def post(self):
        return {}


class OutboundSMSAPI(Resource):
    decorators = [auth.login_required]

    def post(self):
        return {}

api.add_resource(InboundSMSAPI, '/inbound/sms')
api.add_resource(OutboundSMSAPI, '/outbound/sms')
