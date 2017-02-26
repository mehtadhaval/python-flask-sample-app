import json
import time
import unittest
from base64 import b64encode
from datetime import timedelta

from app import app, views, redis_store
from app.models import Account, PhoneNumber


class UnitTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()


class TestCaseAuthHelper:

    @staticmethod
    def get_auth_headers(account):
        return {
            'Authorization': 'Basic ' + b64encode((account.username + ':' + account.auth_id).encode('utf-8'))
                .decode('utf-8'),
            'Content-Type': 'application/json'
        }


class InputParserTestCaseMixin:

    def get_headers(self):
        account = Account.query.first()
        return account, self.get_auth_headers(account)

    def test_method_not_allowed(self):
        res = self.app.get(self.API_URL)
        assert res.status_code == 405

        res = self.app.put(self.API_URL)
        assert res.status_code == 405

        res = self.app.delete(self.API_URL)
        assert res.status_code == 405

    def test_unauthorized_user(self):
        res = self.app.post(self.API_URL, data={
            "from": None
        })
        assert res.status_code == 403

    def test_invalid_data(self):
        account, headers = self.get_headers()
        res = self.app.post(self.API_URL, headers=headers, data=json.dumps({"from": "dummy"}))
        assert res.status_code == 400
        data = json.loads(res.data.decode())
        assert "is invalid" in data.get("error")
        assert data.get("message") is ""


class InboundAPITestCase(TestCaseAuthHelper, InputParserTestCaseMixin, UnitTestCase):

    API_URL = "/inbound/sms"

    def test_invalid_to_number(self):
        account, headers = self.get_headers()
        res = self.app.post(self.API_URL, headers=headers, data=json.dumps(
            {"from": "1234567890", "to": "99999999", "text": "Test"}
        ))
        assert res.status_code == 400
        data = json.loads(res.data.decode())
        assert data.get("error") == "to parameter not found"
        assert data.get("message") is ""

    @staticmethod
    def verify_valid_response(res):
        assert res.status_code == 200
        data = json.loads(res.data.decode())
        assert data.get("error") == ""
        assert data.get("message") == "inbound sms ok"

    def test_valid_data(self):
        account, headers = self.get_headers()
        phone_number = PhoneNumber.query.first()
        from_number = "1234567890"
        to_number = phone_number.number

        # clear from redis
        redis_key = views.get_redis_key("STOP", from_number, to_number)
        redis_store.delete(redis_key)

        # test with dummy data
        res = self.app.post(self.API_URL, headers=headers, data=json.dumps(
            {"from": from_number, "to": phone_number.number, "text": "DUMMY"}
        ))
        self.verify_valid_response(res)
        assert redis_store.get(redis_key) is None

        # test with actual STOP data
        res = self.app.post(self.API_URL, headers=headers, data=json.dumps(
            {"from": from_number, "to": phone_number.number, "text": "STOP"}
        ))
        self.verify_valid_response(res)
        assert redis_store.get(redis_key)


class OutboundAPITestCase(TestCaseAuthHelper, InputParserTestCaseMixin, UnitTestCase):

    API_URL = "/outbound/sms"

    @staticmethod
    def verify_valid_response(res):
        assert res.status_code == 200
        data = json.loads(res.data.decode())
        assert data.get("error") == ""
        assert data.get("message") == "outbound sms ok"

    def test_stop_message(self):
        account, headers = self.get_headers()
        phone_number = PhoneNumber.query.first()
        from_number = "1234567890"
        to_number = phone_number.number

        # add key to redis
        redis_key = views.get_redis_key("STOP", from_number, to_number)
        redis_store.set(redis_key, True, timedelta(seconds=app.config['SMS_THROTTLE_SECONDS']))

        res = self.app.post(self.API_URL, headers=headers, data=json.dumps(
            {"from": from_number, "to": phone_number.number, "text": "DUMMY"}
        ))
        assert res.status_code == 400
        data = json.loads(res.data.decode())
        assert data.get("error") == "sms from {0} to {1} blocked by STOP request".format(from_number, to_number)

    def test_invalid_from_message(self):
        account, headers = self.get_headers()
        phone_number = PhoneNumber.query.filter(PhoneNumber.account_id != account.id).first()
        to_number = "1234567890"
        from_number = phone_number.number

        # remove key from redis
        redis_key = views.get_redis_key("STOP", from_number, to_number)
        redis_store.delete(redis_key)

        res = self.app.post(self.API_URL, headers=headers, data=json.dumps(
            {"from": from_number, "to": phone_number.number, "text": "DUMMY"}
        ))
        assert res.status_code == 400
        data = json.loads(res.data.decode())
        assert data.get("error") == "from parameter not found"

    def test_valid_outbound_message(self):
        account, headers = self.get_headers()
        phone_number = PhoneNumber.query.filter(PhoneNumber.account_id == account.id).first()
        to_number = "1234567890"
        from_number = phone_number.number

        # remove key from redis
        redis_key = views.get_redis_key("STOP", from_number, to_number)
        redis_store.delete(redis_key)

        res = self.app.post(self.API_URL, headers=headers, data=json.dumps(
            {"from": from_number, "to": phone_number.number, "text": "DUMMY"}
        ))
        self.verify_valid_response(res)

    def test_outbound_throttle(self):
        account, headers = self.get_headers()
        phone_number = PhoneNumber.query.filter(PhoneNumber.account_id == account.id).first()
        to_number = "1234567890"
        from_number = phone_number.number

        # remove key from redis
        redis_store.delete(
            views.get_redis_key("STOP", from_number, to_number),
            views.get_redis_key("FROM_THROTTLE", from_number)
        )

        throttle = 5  # set throttle rate to 5 per 10 seconds
        throttle_time = 10

        # set custom throttle rate
        app.config['SMS_THROTTLE_SECONDS'] = throttle_time
        app.config['SMS_THROTTLE_MAX_COUNT'] = throttle

        for i in range(throttle):
            # exhaust number of valid attempts
            res = self.app.post(self.API_URL, headers=headers, data=json.dumps(
                {"from": from_number, "to": phone_number.number, "text": "DUMMY"}
            ))
            self.verify_valid_response(res)

        # verify that request is being throttled
        res = self.app.post(self.API_URL, headers=headers, data=json.dumps(
            {"from": from_number, "to": phone_number.number, "text": "DUMMY"}
        ))
        assert res.status_code == 400
        data = json.loads(res.data.decode())
        assert data.get("error") == "limit reached for from {0}".format(from_number)

        # wait for throttle key to timeout
        time.sleep(throttle_time)

        # try again, should succeed
        res = self.app.post(self.API_URL, headers=headers, data=json.dumps(
            {"from": from_number, "to": phone_number.number, "text": "DUMMY"}
        ))
        self.verify_valid_response(res)


if __name__ == '__main__':
    unittest.main()
