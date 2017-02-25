from functools import wraps

from werkzeug.exceptions import HTTPException


def error_handler(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            res = f(*args, **kwargs)
            return res
        except HTTPException:
            raise
        except Exception:
            return {
                "message": "", "error": "unknown failure"
            }, 500
    return decorated
