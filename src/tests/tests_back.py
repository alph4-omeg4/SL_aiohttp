from faker import Faker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool

import db
from models.models import User
from security import generate_password, check_password

DB_URL = 'postgresql+asyncpg://admin:admin@localhost/postgres'
engine = create_async_engine(DB_URL, poolclass=NullPool)


def test_generate_password():
    user_password = 'admin'
    hashed = generate_password(user_password)
    assert check_password(user_password, hashed)


async def test_create_user():
    fake = Faker()
    test_profile = {'name': fake.first_name(),
                    'surname': fake.last_name(),
                    'login': 'faker',
                    'password': fake.password(),
                    'birthdate': fake.past_datetime(),
                    'blocked': False,
                    'admin': True,
                    'readonly': False
                    }
    print(test_profile)

    test_user = User.parse_obj(test_profile)

    async with engine.begin() as conn:
        res = await db.create_user(conn, test_user)
        assert res.text == 'User faker successfully created.'


async def test_get_all_users():
    async with engine.begin() as conn:
        res = await db.get_all_users(conn)
        assert res


async def test_get_one_user():
    user = 'admin'
    async with engine.begin() as conn:
        res = await db.get_one_user(conn, user)
        assert res


async def test_update_user():
    fake = Faker()

    test_u_profile = {'name': fake.first_name(),
                      'surname': fake.last_name(),
                      'login': 'faker',
                      'password': fake.word(),
                      'birthdate': fake.past_datetime(),
                      'blocked': False,
                      'admin': True,
                      'readonly': False
                      }
    print(f'update data {test_u_profile}')
    test_u_user = User.parse_obj(test_u_profile)

    async with engine.begin() as conn:
        res = await db.update_user(conn, test_u_user)
        assert res.text == 'User faker successfully  updated.'


async def test_delete_user():
    user = 'faker'
    async with engine.begin() as conn:
        res = await db.delete_user(conn, user)
        assert res
