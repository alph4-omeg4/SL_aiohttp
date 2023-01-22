import datetime
import asyncio
from sqlalchemy import create_engine


from database.db import create_user, get_all_users, get_one_user, delete_user, update_user
from database.db_schema import metadata
from models.models import User
from security import check_password

admin_profile = {'name': 'admin11',
                 'surname': 'admin11',
                 'login': 'admin111',
                 'password': 'admin11',
                 'birthdate': datetime.datetime(1970, 1, 1, 0, 0),
                 'blocked': False,
                 'admin': True,
                 'readonly': False
                 }

admin_profile2 = {'name': 'tester_2',
                  'surname': 'admin121',
                  'login': 'admin11',
                  'password': 'admin121',
                  'birthdate': datetime.datetime(1970, 1, 1, 0, 0),
                  'blocked': False,
                  'admin': True,
                  'readonly': True
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
    admin_data2 = User.parse_obj(admin_profile2)
    with engine.begin() as conn:
        c = await create_user(conn, admin_data)
        print(c.text)
        c1 = await create_user(conn, admin_data2)
        print(c1.text)
        # al = await get_all_users(conn)
        # print(al.text)
        g1 = await get_one_user(conn, 'admin11')
        kek = 'password'
        pw = g1[f'{kek}']
        # print(f"----------------------------------{g1['blocked']}")
        print(g1)
        print(type(g1))
        # a = await delete_user(conn, 'admin1221')
        # print(a)
        # up = await update_user(conn, admin_data2)
        # print(up.text)
        password_hash = pw
        password = 'admin122'
        pwb = check_password(password, password_hash)
        print(pwb)

asyncio.run(main())
