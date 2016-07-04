import unittest
import requests
import sys
from os.path import dirname, join

SITE_URL = 'https://www.google.com/'
BROKEN_SITE_URL = 'http://foobar.foo'
BROKEN_SITE_ERROR = (
    b'400: Error: Failed loading page http://foobar.foo (sometimes it will work'
    b' just to ignore this error with --load-error-handling ignore) Exit with'
    b' code 1 due to network error: HostNotFoundError ')


class PlanktonAPITestCase(unittest.TestCase):
    maxDiff = 100500

    def api_url(self, url):
        return '{}{}'.format('http://127.0.0.1:8080', url)

    def test_alive_returns_200_ok(self):
        response = requests.get(self.api_url('/'))
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json['isAlive'], True)

    def test_html_to_pdf_without_options_returns_200_ok(self):
        data = {
            'page': SITE_URL
        }

        response = requests.post(self.api_url('/html-to-pdf/'), json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'application/pdf')

    def test_html_to_pdf_with_empty_options_returns_400(self):
        data = {}

        response = requests.post(self.api_url('/html-to-pdf/'), json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'{"page": "required field"}')

        # Try without data
        response = requests.post(self.api_url('/html-to-pdf/'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'400: You should provide valid json body.')

    def test_html_to_pdf_when_page_is_not_url_returns_400(self):
        data = {'page': "Is not url"}

        response = requests.post(self.api_url('/html-to-pdf/'), json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'{"page": "Please specify correct url"}')

    def test_html_to_pdf_when_wkhtmltopdf_raises_error_returns_400(self):
        data = {'page': BROKEN_SITE_URL}

        response = requests.post(self.api_url('/html-to-pdf/'), json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, BROKEN_SITE_ERROR)


if __name__ == '__main__':

    BASE_DIR = dirname(dirname(__file__))
    sys.path.insert(0, join(BASE_DIR, 'plankton'))

    unittest.main(failfast=True)


