import asyncpgsa
from aiohttp import web
from sqlalchemy import select
from database.db_schema import users, rights
from security import generate_password
from src.models.models import User


def construct_db_url(config):
    db_url = "postgresql://{user}:{password}@{host}:{port}/{database}"
    return db_url.format(
        user=config['DB_USER'],
        password=config['DB_PASS'],
        database=config['DB_NAME'],
        host=config['DB_HOST'],
        port=config['DB_PORT'],
    )


async def init_db(app):
    db_url = construct_db_url(app['config']['database'])
    pool = await asyncpgsa.create_pool(dsn=db_url)
    app['db_pool'] = pool
    return pool

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
        conn.execute(create_user_body_q)

        rights_fields = {"user_login": user.login,
                         "blocked": user.blocked,
                         "admin": user.admin,
                         "readonly": user.readonly}
        create_user_rights_q = rights.insert().values(rights_fields)
        conn.execute(create_user_rights_q)
        return web.HTTPCreated(text=f'User {user.login} successfully created.')
    except Exception as e:
        # print(type(e))   sql integrity catch
        return web.HTTPBadRequest(text='User exists, or 2rights (admin OR readonly')

# ------------------------------------------Read

columns_to_show = [users.c.name,
                   users.c.surname,
                   users.c.login,
                   users.c.password,
                   users.c.birthdate,
                   rights.c.blocked,
                   rights.c.admin,
                   rights.c.readonly]


async def get_all_users(conn):
    all_users_q = select(columns_to_show).select_from(users.join(rights))
    all_users = conn.execute(all_users_q)
    return all_users.mappings().all()


async def get_one_user(conn, login):
    get_one_user_q = select(columns_to_show).select_from(users.join(rights)).where(users.c.login == login)
    one_user = conn.execute(get_one_user_q)
    return one_user.mappings().one()


# ------------------------------------------Update


async def update_user(conn, user: User):
    body_fields = {'name': user.name,
                   'surname': user.surname,
                   'login': user.login,
                   'password': user.password,
                   'birthdate': user.birthdate}
    update_user_body_q = users.update().values(body_fields).where(users.c.login == user.login)
    conn.execute(update_user_body_q)

    rights_fields = {"user_login": user.login,
                     "blocked": user.blocked,
                     "admin": user.admin,
                     "readonly": user.readonly}
    update_user_rights_q = rights.update().values(rights_fields).where(rights.c.user_login == user.login)
    conn.execute(update_user_rights_q)
    return web.HTTPResetContent(text=f'User {user.login} successfully  updated.')


# ------------------------------------------Delete


async def delete_user(conn, login):
    delete_user_q = users.delete().where(users.c.login == login)
    conn.execute(delete_user_q)
    # return web.HTTPNoContent()
    # по идее надо 204 но с ним не должно быть тела респонса
    return web.HTTPOk(text=f"User {login} successfully deleted.")
