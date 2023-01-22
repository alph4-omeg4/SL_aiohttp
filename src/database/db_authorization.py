import logging
from aiohttp_security.abc import AbstractAuthorizationPolicy
from sqlalchemy import create_engine

from src.database import db

log = logging.getLogger(__name__)


DB_URL = 'postgresql://admin:admin@localhost/postgres'
engine = create_engine(DB_URL)


class DBAuthorizationPolicy(AbstractAuthorizationPolicy):

    def __init__(self, db_pool):
        self.db_pool = db_pool
        self.engine = engine

    async def authorized_userid(self, identity):
        log.debug(f'requested AUTH check for {identity}')
        with engine.begin() as conn:
            user = await db.get_one_user(conn, identity)
            if user:
                log.debug(f'AUTH for {identity} confirmed')
                return identity
            else:
                return None


    async def permits(self, identity, permission, context=None):
        log.debug(f'requested PERM check for {identity}')
        with engine.begin() as conn:
            user = await db.get_one_user(conn, identity)
            if not user['blocked']:
                if user["admin"] or user[f"{permission}"]:  # если добавятся новые пермисы тут ничего менять даже не надо
                    log.debug(f'PERM for {identity} granted')
                    return True

            return False
