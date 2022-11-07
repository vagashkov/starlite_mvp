from starlite import Starlite, get


@get("/")
def employees_list() -> dict[str, str]:
    """Keeping the tradition alive with hello world."""
    return {"CEO": "Ivan Marakasoff"}


app = Starlite(route_handlers=[employees_list])
