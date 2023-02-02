import datetime
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

from database.db import create_user
from database.db_schema import metadata
from models.models import User


DB_URL = 'postgresql+asyncpg://admin:admin@localhost/postgres'
mapping = {
    'pool_size': 10,
    'max_overflow': 10,
    'pool_timeout': 30,
    'pool_recycle': 1800
}

engine = create_async_engine(DB_URL, **mapping)


admin_profile = {'name': 'admin',
                 'surname': 'admin',
                 'login': 'admin',
                 'password': 'admin',
                 'birthdate': datetime.date(1970, 1, 1),
                 'blocked': False,
                 'admin': True,
                 'readonly': False
                 }


async def main():
    admin_data = User.parse_obj(admin_profile)
    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)
        await create_user(conn, admin_data)


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
