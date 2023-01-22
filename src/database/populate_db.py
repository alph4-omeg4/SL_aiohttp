import datetime
import asyncio
from sqlalchemy import create_engine

from database.db import create_user
from database.db_schema import metadata
from models.models import User


admin_profile = {'name': 'admin',
                 'surname': 'admin',
                 'login': 'admin',
                 'password': 'admin',
                 'birthdate': datetime.date(1970, 1, 1),
                 'blocked': False,
                 'admin': True,
                 'readonly': False
                 }


DB_URL = 'postgresql://admin:admin@localhost/postgres'
mapping = {
    'pool_size': 10,
    'max_overflow': 10,
    'pool_timeout': 30,
    'pool_recycle': 1800
}

engine = create_engine(DB_URL, **mapping)


async def main():
    metadata.drop_all(engine)
    metadata.create_all(engine)
    admin_data = User.parse_obj(admin_profile)

    with engine.begin() as conn:
        await create_user(conn, admin_data)


asyncio.run(main())
