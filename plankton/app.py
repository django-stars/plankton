import argparse
from aiohttp import web
from plankton.routes import routes
import plankton.settings


def init_app():
    parser = argparse.ArgumentParser(description='Plankton - wkhtmltopdf REST service')

    parser.add_argument('--wkhtmltopdf_command', nargs='?',
                        help='wkhtmltopdf command (default wkhtmltopdf)')
    parser.add_argument('--port', nargs='?', type=int,
                        help='server port (default 8080)', default=8080)
    args = parser.parse_args()

    if args.wkhtmltopdf_command:
        plankton.settings.WKHTMLTOPDF_CMD = args.wkhtmltopdf_command

    app = web.Application()
    for route in routes:
        app.router.add_route(*route)

    web.run_app(app, port=args.port)

