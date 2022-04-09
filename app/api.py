from aiohttp import web


routes = web.RouteTableDef()


@routes.get("/leagues")
async def get_leagues(request: web.Request) -> web.Response:
    pass


@routes.post("/leagues")  # admin
async def create_league(request: web.Request) -> web.Response:
    pass


@routes.get("/leagues/active")
async def get_active_leagues(request: web.Request) -> web.Response:
    pass


@routes.get(r"/leagues/{league:\d+}")
async def get_league(request: web.Request) -> web.Response:
    pass


@routes.put(r"/leagues/{league:\d+}")  # admin
async def edit_league(request: web.Request) -> web.Response:
    pass


@routes.delete(r"/leagues/{league:\d+}")  # admin
async def delete_league(request: web.Request) -> web.Response:
    pass


@routes.get(r"/leagues/{league:\d+}/participants")
async def get_league_participants(request: web.Request) -> web.Response:
    pass


@routes.post(r"/leagues/{league:\d+}/participants")  # admin
async def add_league_participant(request: web.Request) -> web.Response:
    pass


@routes.delete(r"/leagues/{league:\d+}/participants/{participant:\d+}")  # admn
async def remove_league_participants(request: web.Request) -> web.Response:
    pass


@routes.post(r"/leagues/{league:\d+}/start")  # admin
async def start_league(request: web.Request) -> web.Response:
    pass


@routes.post(r"/leagues/{league:\d+}/stop")  # admin
async def stop_league(request: web.Request) -> web.Response:
    pass


@routes.get("/users")
async def get_users(request: web.Request) -> web.Response:
    """
    Get players.
    response: [{user_id, name}, …]
    """


@routes.post("/users")  # admin
async def create_user(request: web.Request) -> web.Response:
    """
    Create player.
    request: {name}
    response: {user_id, name, password (auto-generated)}
    """


@routes.get(r"/users/{user:\w+}")
async def get_user(request: web.Request) -> web.Response:
    """
    Get a certain user.
    response: {user_id, name}
    """


@routes.delete(r"/users/{user:\w+}")  # admin
async def delete_user(request: web.Request) -> web.Response:
    """
    Delete player.
    request: empty
    response: empty
    """
