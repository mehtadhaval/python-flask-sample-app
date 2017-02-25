from app import app
from app.models import Account, PhoneNumber


@app.route('/inbound/sms', methods=["POST"])
def inbound_sms():
    return ""


@app.route('/outbound/sms', methods=["POST"])
def outbound_sms():
    return ""
