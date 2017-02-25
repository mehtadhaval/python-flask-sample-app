import flask_restful
import six
from flask_restful import reqparse, inputs
from flask_restful.reqparse import Argument


def abort(status_code=200, error=None, message=None):
    result = {"message": "", "error": ""}
    if error:
        result["error"] = error
    if message:
        result["message"] = message
    flask_restful.abort(status_code, **result)


class CustomArgument(Argument):

    def handle_validation_error(self, error, bundle_errors):
        """
        Adds custom validation messages
        """
        error_str = six.text_type(error)
        if "Missing required parameter" in error_str:
            msg = "{} is missing".format(self.name)
        else:
            msg = "{} is invalid".format(self.name)
        if bundle_errors:
            return error, msg
        abort(400, error=msg)


def get_parser():
    parser = reqparse.RequestParser()
    parser.add_argument(CustomArgument('from', required=True, type=inputs.regex('^[0-9]{6,16}$')))
    parser.add_argument(CustomArgument('to', required=True, type=inputs.regex('^[0-9]{6,16}$')))
    parser.add_argument(CustomArgument('text', required=True, type=inputs.regex('^[0-9a-zA-Z\r\n ]{1,120}$')))
    return parser
