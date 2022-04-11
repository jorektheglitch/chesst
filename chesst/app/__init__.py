"""
Here is all things about aiohttp application like description of handlers,
routes, creating and running an application.
"""


from .api import routes
from ..config import Config

from aiohttp import web


def run(config: Config) -> None:
    app = web.Application()
    app.router.add_routes(routes)
    settings = config.app
    web.run_app(app, host=settings.host, port=settings.port)
