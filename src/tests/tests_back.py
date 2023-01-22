import datetime
from sqlalchemy import create_engine

import db
from security import generate_password, check_password

DB_URL = 'postgresql://admin:admin@localhost/postgres'
engine = create_engine(DB_URL)


def test_generate_password():
    user_password = 'admin'
    hashed = generate_password(user_password)
    assert check_password(user_password, hashed)


async def test_create_user():
    test_c_profile = {'name': 'tester',
                      'surname': 'tester',
                      'login': 'tester',
                      'password': 'tester',
                      'birthdate': datetime.date(1970, 1, 1),
                      'blocked': False,
                      'admin': True,
                      'readonly': False
                      }
    # with engine.begin() as conn:
    #     res = await db.create_user(conn, test_profile)
    #     assert


async def test_get_all_users():
    with engine.begin() as conn:
        res = await db.get_all_users(conn)
        assert res


async def test_get_one_user():
    user = 'admin'
    with engine.begin() as conn:
        res = await db.get_one_user(conn, user)
        assert res


async def test_update_user():
    pass
    test_u_profile = {'name': 'admint',
                      'surname': 'admint',
                      'login': 'admin',
                      'password': 'admint',
                      'birthdate': datetime.date(1970, 1, 1),
                      'blocked': False,
                      'admin': True,
                      'readonly': False
                      }

    with engine.begin() as conn:
        res = await db.update_user(conn, test_u_profile)
        print(res)



async def test_delete_user():
    user = 'admin'
    # with engine.begin() as conn:
    #     res = await db.delete_user(conn, user)
