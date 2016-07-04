from copy import copy

import validators
from cerberus.cerberus import Validator

options_schema = {
    # Page options
    'javascript-delay': {'type': 'integer'},


    # Headers And Footer Options
    'footer-center': {'type': 'string'},
    'footer-font-name': {'type': 'string'},
    'footer-font-size': {'type': 'integer'},
    'footer-html': {'type': 'string'},
    'footer-left': {'type': 'string'},
    'footer-line': {'type': 'boolean'},
    'no-footer-line': {'type': 'boolean'},
    'footer-right': {'type': 'string'},
    'footer-spacing': {'type': 'integer'},
    'header-center': {'type': 'string'},
    'header-font-name': {'type': 'string'},
    'header-font-size': {'type': 'integer'},
    'header-html': {'type': 'string'},
    'header-left': {'type': 'string'},
    'header-line': {'type': 'boolean'},
    'no-header-line': {'type': 'boolean'},
    'header-right': {'type': 'string'},
    'header-spacing': {'type': 'integer'},
    'replace': {'type': 'list'},
}


class WkhtmlToPdfParamsValidator(object):
    def __init__(self):
        self.validator = Validator(
        schema={
            'page': {'type': 'string', 'required': True},
            'options': {'type': 'dict', 'schema': options_schema}
        }
        )
        self.errors = {}

    def validate(self, data):
        self.validator.validate(data)
        self.errors = copy(self.validator.errors)

        if not self.errors:
            if not validators.url(data['page']):
                self.errors['page'] = "Please specify correct url"

        return not bool(self.errors)
