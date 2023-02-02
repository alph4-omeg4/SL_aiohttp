import logging
from aiohttp_security.abc import AbstractAuthorizationPolicy

from src.database import db

log = logging.getLogger(__name__)


class DBAuthorizationPolicy(AbstractAuthorizationPolicy):

    def __init__(self, engine):
        self.engine = engine

    async def authorized_userid(self, identity):
        log.debug(f'requested AUTH check for {identity}')
        async with self.engine.begin() as conn:
            user = await db.get_one_user(conn, identity)
            if user:
                log.debug(f'AUTH for {identity} confirmed')
                return identity
            else:
                return None


    async def permits(self, identity, permission, context=None):
        log.debug(f'requested PERM check for {identity}')
        async with self.engine.begin() as conn:
            user = await db.get_one_user(conn, identity)
            if not user['blocked']:
                if user["admin"] or user[f"{permission}"]:
                    log.debug(f'PERM for {identity} granted')
                    return True

            return False
