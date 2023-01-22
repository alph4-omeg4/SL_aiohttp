import json

from aiohttp import web
from aiohttp.web_request import Request
from aiohttp_security import remember, forget, authorized_userid, check_permission
from sqlalchemy import create_engine

from db import update_user
from models.models import User, UserAuth
from security import generate_password
from src.database import db
from src.form_validation import validate_auth_form

routes = web.RouteTableDef()

DB_URL = 'postgresql://admin:admin@localhost/postgres'
engine = create_engine(DB_URL)


def redirect(route_name):
    location = f'/{route_name}'
    return web.HTTPFound(location)


@routes.get('/', allow_head=False)
async def index(request):

    return web.Response(
        text='/login POST\n/logoff GET\n'
             '/users GET\t\t\t*show all*\n/users POST\t\t\t*create new*\n'
             '/users/{login} GET\t\t*show exact*\n/users/{login} POST\t\t*update exact*\n/users/{login} DELETE\t\t*delete exact*\n'
             '/docs\t\t\t\t*swaggerUI*'
    )


@routes.post('/login')
async def login(request: Request):

    with engine.begin() as conn:
        check_for_valid_error = await validate_auth_form(conn, request)
        if check_for_valid_error:
            return web.HTTPBadRequest(text=check_for_valid_error)
        else:
            user_login = UserAuth.parse_raw(await request.text()).login
            response = web.HTTPOk(text=f'Auth as {user_login} successful')
            await remember(request, response, user_login)
            return response
        return web.HTTPBadRequest(text='Auth failed')



@routes.get('/logout')
async def logout(request:Request):
    response = web.HTTPOk(text='Logged off')
    await forget(request, response)
    return response


# -------------------------------------------------------------------------------------------------------------------


@routes.get('/users')
async def get_all_users_view(request: Request):
    await check_permission(request, 'readonly')

    with engine.begin() as conn:
        username = await authorized_userid(request)
        all_users = await db.get_all_users(conn)
        model_all_users = [User.parse_obj(user) for user in all_users]
        dict_all_users = [model_user.json() for model_user in model_all_users]
        jsoned_all_users = [json.loads(dict_user) for dict_user in dict_all_users]

        for jsoned_user in jsoned_all_users:
            del jsoned_user['password']
        # [del jsoned_user['password'] for jsoned_user in jsoned_all_user] почитать почему дел в компрехэнш не работает
        return web.json_response(jsoned_all_users)


@routes.post('/users')
async def create_user_view(request: Request):

    await check_permission(request, 'admin')

    with engine.begin() as conn:
        new_user = User.parse_raw(await request.text())
        new_user.password = generate_password(new_user.password)
        return await db.create_user(conn, new_user)


@routes.get('/users/{login}')
async def get_one_user_view(request:Request):
    await check_permission(request, 'readonly')

    login = request.match_info['login']
    with engine.begin() as conn:
        user = await db.get_one_user(engine, login)
        model_user = User.parse_obj(user)
        dict_user = model_user.json()
        jsoned_user = json.loads(dict_user)
        del jsoned_user['password']
        return web.json_response(jsoned_user)


@routes.post('/users/{login}')
async def update_user_view(request:Request):
    await check_permission(request, 'admin')

    login = request.match_info['login']
    with engine.begin() as conn:
        user_model = User.parse_raw(await request.text())
        user_dict = user_model.dict()
        # пароль шифруется ниже его можно тоже менять
        if user_dict['login'] != login:
            raise web.HTTPNonAuthoritativeInformation(text='Error: Wrong login')
        return await update_user(conn, user_model)



@routes.delete('/users/{login}')
async def delete_user_view(request: Request):
    await check_permission(request, 'admin')

    login = request.match_info['login']
    with engine.begin() as conn:
        return await db.delete_user(conn, login)