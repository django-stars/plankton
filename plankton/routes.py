from wkhtmltopdf.views import HtmlToPdfView


routes = (
    ('POST', '/html-to-pdf/', HtmlToPdfView),
)
