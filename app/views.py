from app import app
from app.auth import auth


@auth.login_required
@app.route('/inbound/sms', methods=["POST"])
def inbound_sms():
    return ""


@auth.login_required
@app.route('/outbound/sms', methods=["POST"])
def outbound_sms():
    return ""
