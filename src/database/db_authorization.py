from aiohttp_security.abc import AbstractAuthorizationPolicy
from sqlalchemy import create_engine

from security import check_password
from src.database import db


DB_URL = 'postgresql://admin:admin@localhost/postgres'


engine = create_engine(DB_URL)


class DBAuthorizationPolicy(AbstractAuthorizationPolicy):

    def __init__(self, db_pool):
        self.db_pool = db_pool
        self.engine = engine

    async def authorized_userid(self, identity):

        with engine.begin() as conn:
            user = await db.get_one_user(conn, identity)
            if user:
                return identity
            else:
                return None


    async def permits(self, identity, permission, context=None):

        with engine.begin() as conn:
            user = await db.get_one_user(conn, identity)
            if not user['blocked']:

                if user["admin"]:
                    return True

                if user[f"{permission}"]:   # если добавятся новые пермисы тут ничего менять даже не надо
                    return True

            return False


async def check_credentials(_, login, password):
    with engine.begin() as conn:
        user = await db.get_one_user(conn, login)
        if user is not None:
            password_hash = user['password']

            return check_password(password_hash, password)
    return False
