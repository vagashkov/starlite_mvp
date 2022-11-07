from starlite import Starlite, get

employees_data = {"staff_list": [
    {"id": 1, 'post': "CEO", 'name': "Ivan Marakasoff"},
    {'id': 2, 'post': "CLO", 'name': "Top Lawyer"},
    {'id': 3, 'post': "CIO", 'name': "Kilobit Megabitov"},
    {'id': 4, 'post': "CFO", 'name': "Giveme Moremoney"}]
}


@get("/")
def employees_list() -> dict[str, str]:
    """Keeping the tradition alive with hello world."""
    return employees_data


@get("/0/details")
def employee_details() -> dict[str, str]:
    """Keeping the tradition alive with hello world."""
    return employees_data['staff_list'][0]


app = Starlite(route_handlers=[employees_list, employee_details])
