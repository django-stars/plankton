from aiohttp import web
from routes import routes


def init_app():
    app = web.Application()
    for route in routes:
        app.router.add_route(*route)

    return app
