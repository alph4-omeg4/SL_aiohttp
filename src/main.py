
from aiohttp import web
from aiohttp_security import SessionIdentityPolicy
from aiohttp_security import authorized_userid
from aiohttp_security import setup as setup_security
from aiohttp_session import setup as setup_session
import aiohttp_session
from aiohttp_swagger import *


from views import routes, index
from src.database.db_authorization import DBAuthorizationPolicy
from src.database.db import init_db
from src.settings import load_config, CONFIG_PATH

config = load_config(CONFIG_PATH)


async def current_user(request):
    username = await authorized_userid(request)
    is_anonymous = not bool(username)
    return {'current_user': {'is_anonymous': is_anonymous}}

#
# async def init_redis(app):
#     redis_host = app["config"]["redis"]["REDIS_HOST"]
#     redis_port = app["config"]["redis"]["REDIS_PORT"]
#     print(f"redis://{redis_host}:{redis_port}")
#     redis_s = redis.from_url(f"redis://{redis_host}:{redis_port}")
#     # redis1 = redis.Redis()
#     # redis1.ping()
#     redis_s.ping()
#     print(redis_s.ping)
#     app["redis"] = redis
#     print(type(redis_s))
#     return redis_s


async def init_app(config):

    app = web.Application()

    app['config'] = config

    app.router.add_routes(routes)

    db_pool = await init_db(app)

    app.router.add_route('GET', "/", index)

    setup_session(app, aiohttp_session.SimpleCookieStorage())

    setup_security(app,
                   SessionIdentityPolicy(),
                   DBAuthorizationPolicy(db_pool))
    setup_swagger(app, swagger_url="/docs", swagger_from_file="swagger.json")

    # s = SwaggerDocs(app, components="sl_swag.yaml", swagger_ui_settings=SwaggerUiSettings(path="/docs"))
    # s.add_routes(routes)

    return app


def main():
    app = init_app(config)
    web.run_app(app, host=config['base']['HOST'], port=config['base']['PORT'])


if __name__ == '__main__':
    main()
