import json
import logging
from aiohttp import web
from aiohttp.web_request import Request
from aiohttp_security import remember, forget, authorized_userid, check_permission

from database.db import update_user
from models.models import User, UserAuth, UserOne, UserMany
from security import generate_password
from src.database import db
from src.form_validation import validate_auth_form

routes = web.RouteTableDef()

DB_URL = 'postgresql+asyncpg://admin:admin@localhost/postgres'
# engine = create_async_engine(DB_URL)

log = logging.getLogger(__name__)


def redirect(route_name):
    location = f'/{route_name}'
    return web.HTTPFound(location)


@routes.get('/', allow_head=False)
async def index(request):
    log.debug('index page req')
    return web.Response(
        text='/login POST\n/logoff GET\n'
             '/users GET\t\t\t*show all*\n/users POST\t\t\t*create new*\n'
             '/users/{login} GET\t\t*show exact*\n/users/{login} POST\t\t*update exact*\n/users/{login} DELETE\t\t*delete exact*\n'
             '/docs\t\t\t\t*swaggerUI*'
    )


@routes.post('/login')
async def login(request: Request):
    log.debug('login request')
    engine = request.app['engine']
    async with engine.begin() as conn:
        check_for_valid_error = await validate_auth_form(conn, request)
        if check_for_valid_error:
            return web.HTTPBadRequest(text=check_for_valid_error)
        else:
            user_login = UserAuth.parse_raw(await request.text()).login
            log.debug(f'Auth as {user_login} successful')
            response = web.HTTPOk(text=f'Auth as {user_login} successful')
            await remember(request, response, user_login)
            return response




@routes.get('/logout')
async def logout(request: Request):
    log.debug('logged out')
    response = web.HTTPOk(text='Logged off')
    await forget(request, response)
    return response


# -------------------------------------------------------------------------------------------------------------------


@routes.get('/users')
async def get_all_users_view(request: Request):
    log.debug('get user list req, checking PERM')
    await check_permission(request, 'readonly')
    log.debug('get user list req, PERM granted, loading list')
    engine = request.app['engine']
    # не понимаю как корректно избавится от получения транзакции для пуе
    async with engine.begin() as conn:
        all_users = await db.get_all_users(conn)
        # return web.json_response([UserSafe.parse_obj(user).json() for user in all_users])
        return web.json_response(json.loads(UserMany(items=all_users).json()))


@routes.post('/users')
async def create_user_view(request: Request):
    log.debug('create user req, checking PERM')
    await check_permission(request, 'admin')
    log.debug('create user req, PERM granted, creating user')
    engine = request.app['engine']
    async with engine.begin() as conn:
        new_user = User.parse_raw(await request.text())
        new_user.password = generate_password(new_user.password)
        return await db.create_user(conn, new_user)


@routes.get('/users/{login}')
async def get_one_user_view(request: Request):
    log.debug('get exact user req, checking PERM')
    await check_permission(request, 'admin')
    log.debug('create user req, PERM, granted, fetching user')
    login = request.match_info['login']
    engine = request.app['engine']
    async with engine.begin() as conn:
        user = await db.get_one_user(conn, login)
        # return web.json_response(UserSafe.parse_obj(user).json())
        return web.json_response(json.loads(UserOne(item=user).json()))


@routes.post('/users/{login}')
async def update_user_view(request: Request):
    log.debug('change user req, checking PERM')
    await check_permission(request, 'admin')
    log.debug('change user req, PERM granted, updaintg')
    login = request.match_info['login']
    engine = request.app['engine']
    async with engine.begin() as conn:
        user_model = User.parse_raw(await request.text())
        user_dict = user_model.dict()
        if user_dict['login'] != login:
            raise web.HTTPNonAuthoritativeInformation(text='Error: Wrong login')
        return await update_user(conn, user_model)



@routes.delete('/users/{login}')
async def delete_user_view(request: Request):
    log.debug('del user req, checking PERM')
    await check_permission(request, 'admin')
    log.debug('del user req, PERM granted, tryin to del user')
    logged_username = await authorized_userid(request)
    login_to_del = request.match_info['login']
    engine = request.app['engine']
    if not logged_username == login_to_del:
        async with engine.begin() as conn:
            return await db.delete_user(conn, login_to_del)
    else:
        raise web.HTTPForbidden(text='Cant delete self')
