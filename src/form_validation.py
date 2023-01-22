from src.database import db
from src.security import check_password
from models.models import UserAuth


async def validate_auth_form(conn, request):
    user_data = UserAuth.parse_raw(await request.text())
    login = user_data.login
    password = user_data.password
    if not login:
        return 'login is required'
    if not password:
        return 'password is required'

    user = await db.get_one_user(conn, login)
    if not login:
        return 'Invalid login'
    if not check_password(password, user['password']):
        return 'Invalid password'

    return None
