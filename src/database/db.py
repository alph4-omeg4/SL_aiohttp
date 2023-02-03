from aiohttp import web
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine

from database.db_schema import users, rights
from security import generate_password
from src.models.models import User


def construct_db_url(config):
    db_url = "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"
    return db_url.format(
        user=config['DB_USER'],
        password=config['DB_PASS'],
        database=config['DB_NAME'],
        host=config['DB_HOST'],
        port=config['DB_PORT'],
    )


async def init_db(app):

    db_url = construct_db_url(app['config']['database'])
    engine = create_async_engine(db_url)
    app['engine'] = engine
    return engine

# --------------------------------------CRUD -------------------------------------------------------------------------

# ------------------------------------------Create


async def create_user(conn, user: User):
    try:
        body_fields = {'name': user.name,
                       'surname': user.surname,
                       'login': user.login,
                       'password': generate_password(user.password),
                       'birthdate': user.birthdate}
        create_user_body_q = users.insert().values(body_fields)
        await conn.execute(create_user_body_q)

        rights_fields = {"user_login": user.login,
                         "blocked": user.blocked,
                         "admin": user.admin,
                         "readonly": user.readonly}
        create_user_rights_q = rights.insert().values(rights_fields)
        await conn.execute(create_user_rights_q)

        return web.HTTPCreated(text=f'User {user.login} successfully created.')
    except Exception as e:
        # print(type(e))  -  sql integrity catch
        return web.HTTPBadRequest(text='User exists, or 2 rights (admin OR readonly')

# ------------------------------------------Read


async def get_all_users(conn):
    all_users = await conn.execute(select(users, rights).select_from(users.join(rights)))
    return all_users.mappings().all()


async def get_one_user(conn, login):
    one_user = await conn.execute(select(users, rights).select_from(users.join(rights)).where(users.c.login == login))
    return one_user.mappings().one()


# ------------------------------------------Update


async def update_user(conn, user: User):
    body_fields = {'name': user.name,
                   'surname': user.surname,
                   'login': user.login,
                   'password': user.password,
                   'birthdate': user.birthdate}
    update_user_body_q = users.update().values(body_fields).where(users.c.login == user.login)
    await conn.execute(update_user_body_q)

    rights_fields = {"user_login": user.login,
                     "blocked": user.blocked,
                     "admin": user.admin,
                     "readonly": user.readonly}
    update_user_rights_q = rights.update().values(rights_fields).where(rights.c.user_login == user.login)
    await conn.execute(update_user_rights_q)
    return web.HTTPResetContent(text=f'User {user.login} successfully  updated.')


# ------------------------------------------Delete


async def delete_user(conn, login):
    await conn.execute(users.delete().where(users.c.login == login))
    return web.HTTPNoContent()

