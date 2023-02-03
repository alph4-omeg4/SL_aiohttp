import logging
import aiohttp_session
from aiohttp import web
from aiohttp_security import SessionIdentityPolicy
from aiohttp_security import setup as setup_security
from aiohttp_session import setup as setup_session
from aiohttp_swagger import *

from views import routes
from src.database.db_authorization import DBAuthorizationPolicy
from src.settings import load_config, CONFIG_PATH
from db import init_db

config = load_config(CONFIG_PATH)

log = logging.getLogger(__name__)
log.debug('started')


async def init_app():

    logging.basicConfig(level=logging.DEBUG)

    app = web.Application()

    app['config'] = config
    log.debug(f"init w config {app['config']}")

    app.router.add_routes(routes)

    setup_session(app, aiohttp_session.SimpleCookieStorage())

    engine = await init_db(app)

    setup_security(app,
                   SessionIdentityPolicy(),
                   DBAuthorizationPolicy(engine))

    # setup_swagger(app, swagger_url="/docs", swagger_from_file="./openapi_doc.json")



    log.debug('started')

    return app


def main():
    app = init_app()
    web.run_app(app, host=config['base']['HOST'], port=config['base']['PORT'])


if __name__ == '__main__':
    main()
