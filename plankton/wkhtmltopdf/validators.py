from copy import copy

import validators
from cerberus.cerberus import Validator


options_schema = {
    ### Global options ###

    # Collate when printing multiple copies(default)
    'collate': {'type': 'boolean'},
    # Do not collate when printing multiple copies
    'no-collate': {'type': 'boolean'},
    # Number of copies to print into the pdf file (default 1)
    'copies': {'type': 'integer'},
    # Change the dpi explicitly (this has no effect on X11 based systems)
    'dpi': {'type': 'integer'},
    # Display more extensive help, detailing less common command switches
    'extended-help': {'type': 'boolean'},
    # PDF will be generated in grayscal
    'grayscale': {'type': 'boolean'},
    # When embedding images scale them down to this dpi (default 600)
    'image-dpi': {'type': 'integer'},
    # When jpeg compressing images use this quality (default 94)
    'image-quality': {'type': 'integer'},
    # Generates lower quality pdf/ps. Useful to shrink the result document space
    'lowquality': {'type': 'integer'},
    # Set the page bottom margi
    'margin-bottom': {'type': 'integer'},
    # Set the page left margin (default 10mm)
    'margin-left': {'type': 'integer'},
    # Set the page right margin (default 10mm)
    'margin-right': {'type': 'integer'},
    # Set the page top margin
    'margin-top': {'type': 'integer'},
    # Set orientation to Landscape or Portrait (default Portrait)
    # TODO: custom validation
    'orientation': {'type': 'string'},
    # Page height
    'page-height': {'type': 'integer'},
    # Set paper size to: A4, Letter, etc. (default A4)
    # TODO: custom validation
    'page-size': {'type': 'string'},
    # Page width
    'page-width': {'type': 'integer'},
    # Do not use lossless compression on pdf objects
    'no-pdf-compression': {'type': 'boolean'},
    # Be less verbose
    'quiet': {'type': 'boolean'},
    # The title of the generated pdf file (The title of the first document is used if not specified)
    'title': {'type': 'string'},

    ### Page options ###

    # Do print background (default)
    'background': {'type': 'boolean'},
    # Do not print background
    'no-background': {'type': 'boolean'},
    # Cookies, list of lists [['key1', 'val1'], ['key2'], ['val2']]
    "cookies": {
        'type': 'list',
        'items': [{'type': 'string'}, {'type': 'string'}]
    },
    # Set an additional HTTP headers: [['key1', 'val1'], ['key2'], ['val2']]
    "custom-headers": {
        'type': 'list',
        'items': [{'type': 'string'}, {'type': 'string'}]
    },
    # Add HTTP headers specified by custom-headers for each resource request.
    'custom-header-propagation': {'type': 'boolean'},
    # Do not add HTTP headers specified by custom-headers for each resource request.
    'no-custom-header-propagation': {'type': 'boolean'},
    # Show javascript debugging output
    'debug-javascript': {'type': 'boolean'},
    # Do not show javascript debugging output (default)
    'no-debug-javascript': {'type': 'boolean'},
    # Set the default text encoding, for input
    'encoding': {'type': 'string'},
    # Do not make links to remote web pages
    'disable-external-links': {'type': 'boolean'},
    # Make links to remote web pages (default)
    'enable-external-links': {'type': 'boolean'},
    # Do not turn HTML form fields into pdf form fields (default)
    'disable-forms': {'type': 'boolean'},
    # Turn HTML form fields into pdf form fields
    'enable-forms': {'type': 'boolean'},
    # Do load or print images (default)
    'images': {'type': 'boolean'},
    # Do not load or print images
    'no-images': {'type': 'boolean'},
    # Do not make local links
    'disable-internal-links': {'type': 'boolean'},
    # Make local links (default)
    'enable-internal-links': {'type': 'boolean'},
    # Do not allow web pages to run javascript
    'disable-javascript': {'type': 'boolean'},
    # Do allow web pages to run javascript (default)
    'enable-javascript': {'type': 'boolean'},
    # Wait some milliseconds for javascript finish (default 200)
    'javascript-delay': {'type': 'integer'},
    # Specify how to handle pages that fail to load: abort, ignore or skip (default abort)
    'load-error-handling': {'type': 'string'},
    # Specify how to handle media files that fail to load: abort, ignore or skip (default ignore)
    'load-media-error-handling': {'type': 'string'},
    'minimum-font-size': {'type': 'integer'},
    # Do not include the page in the table of contents and outlines
    'exclude-from-outline': {'type': 'boolean'},
    # Include the page in the table of contents and outlines (default)
    'include-in-outline': {'type': 'boolean'},
    # Set the starting page number (default 0)
    'page-offset': {'type': 'integer'},
    # HTTP Authentication username
    'username': {'type': 'string'},
    # HTTP Authentication password
    'password': {'type': 'string'},
    # Disable installed plugins (default)
    'disable-plugins': {'type': 'boolean'},
    # Enable installed plugins (plugins will likely not work)
    'enable-plugins': {'type': 'boolean'},
    # Add an additional post fields: [['key1', 'val1'], ['key2'], ['val2']]
    'post': {
        'type': 'list',
        'items': [{'type': 'string'}, {'type': 'string'}]
    },
    # Use print media-type instead of screen
    'print-media-type': {'type': 'boolean'},
    # Do not use print media-type instead of screen (default)
    'no-print-media-type': {'type': 'boolean'},
    # Use a proxy
    'proxy': {'type': 'string'},
    # Run this additional javascript after the page is done loading
    'run-scripts': {
        'type': 'list',
        'items': [{'type': 'string'}]
    },
    # Disable the intelligent shrinking strategy
    # used by WebKit that makes the pixel/dpi
    # ratio none constant
    'disable-smart-shrinking': {'type': 'boolean'},
    # Enable the intelligent shrinking strategy
    # used by WebKit that makes the pixel/dpi
    # ratio none constant (default)
    'enable-smart-shrinking': {'type': 'boolean'},
    # Stop slow running javascripts (default)
    'stop-slow-scripts': {'type': 'boolean'},
    # Do not Stop slow running javascripts
    'no-stop-slow-scripts': {'type': 'boolean'},
    # Specify a user style sheet, to load with every page
    'user-style-sheet': {'type': 'string'},
    'no-print-media-type': {'type': 'boolean'},
    # Set viewport size if you have custom
    # scrollbars or css attribute overflow to
    # emulate window size
    'viewport-size': {'type': 'integer'},
    # Wait until window.status is equal to this string before rendering page
    'window-status': {'type': 'string'},
    # Use this zoom factor (default 1)
    'zoom': {'type': 'float'},

    ### Headers And Footer Options ###

    # Centered footer text
    'footer-center': {'type': 'string'},
    # Set footer font name (default Arial)
    'footer-font-name': {'type': 'string'},
    # Set footer font size (default 12)
    'footer-font-size': {'type': 'integer'},
    # Adds a html footer
    'footer-html': {'type': 'string'},
    # Left aligned footer text
    'footer-left': {'type': 'string'},
    # Display line above the footer
    'footer-line': {'type': 'boolean'},
    # Do not display line above the footer (default)
    'no-footer-line': {'type': 'boolean'},
    # Right aligned footer text
    'footer-right': {'type': 'string'},
    # Spacing between footer and content in mm (default 0)
    'footer-spacing': {'type': 'integer'},
    # Centered header text
    'header-center': {'type': 'string'},
    # Set header font name (default Arial)
    'header-font-name': {'type': 'string'},
    # Set header font size (default 12)
    'header-font-size': {'type': 'integer'},
    # Adds a html header
    'header-html': {'type': 'string'},
    # Left aligned header text
    'header-left': {'type': 'string'},
    # Display line below the header
    'header-line': {'type': 'boolean'},
    # Do not display line below the header (default)
    'no-header-line': {'type': 'boolean'},
    # Right aligned header text
    'header-right': {'type': 'string'},
    # Spacing between header and content in mm (default 0)
    'header-spacing': {'type': 'integer'},
    # Replace [name] with value in header and footer (repeatable)
    'replace': {
        'type': 'list',
        'items': [{'type': 'string'}]
    },
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
