from starlite import Starlite, Controller, get

employees_data = {"staff_list": [
    {"id": 1, 'post': "CEO", 'name': "Ivan Marakasoff"},
    {'id': 2, 'post': "CLO", 'name': "Top Lawyer"},
    {'id': 3, 'post': "CIO", 'name': "Kilobit Megabitov"},
    {'id': 4, 'post': "CFO", 'name': "Giveme Moremoney"}]
}


class EmployeeController(Controller):
    path = '/employees'

    @get()
    def employees_list(self) -> dict[str, str]:
        return employees_data

    @get("/{emp_id: int}")
    def employee_details(self, emp_id: int) -> dict[str, str]:
        return employees_data['staff_list'][emp_id]


app = Starlite(route_handlers=[EmployeeController])
