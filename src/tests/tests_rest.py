from main import init_app


async def test_index(aiohttp_client):
    client = await aiohttp_client(await init_app())
    resp = await client.get("/")
    assert resp.status == 200


async def test_login(aiohttp_client):
    client = await aiohttp_client(await init_app())
    body = {"login": "admin", "password": "admin"}
    resp = await client.post("/login", json=body)
    text = await resp.text()
    assert text == 'Auth as admin successful'
    assert resp.status == 200


async def test_logout(aiohttp_client):
    client = await aiohttp_client(await init_app())
    resp = await client.get("/logout")
    text = await resp.text()
    print(text)
    assert text == 'Logged off'
    assert resp.status == 200


async def test_get_all_users(aiohttp_client):
    client = await aiohttp_client(await init_app())
    resp = await client.get("/users")
    text = await resp.text()
    assert text
    assert resp.status
    #------------------------------------------------------------------- не понимаю как сделаьт фикстуру авторизации


async def test_get_one_user(aiohttp_client):
    client = await aiohttp_client(await init_app())
    body = {"login": "admin"}
    resp = await client.get("/users/admin", json=body)
    text = resp.text()
    # assert text = usermodel
    assert resp.status


async def test_create_user(aiohttp_client):
    client = await aiohttp_client(await init_app())
    # body = usermodel
    resp = await client.post("/users")
    assert resp.status


async def test_update_user(aiohttp_client):
    client = await aiohttp_client(await init_app())
    # body = usermodel
    resp = await client.post("/user/tester")
    assert resp.status


async def test_delete_one_user(aiohttp_client):
    client = await aiohttp_client(await init_app())
    body = {"login": "admin"} # надо создать фикстуру чтоб создала юзера для удаления---------------------------
    resp = await client.post("/user/tester", json=body)
    assert resp.status
