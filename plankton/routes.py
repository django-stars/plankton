from plankton.wkhtmltopdf.views import HtmlToPdfView, alive


routes = (
    ('GET', '/', alive),
    ('POST', '/html-to-pdf/', HtmlToPdfView),
)
