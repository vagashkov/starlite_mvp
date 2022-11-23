from datetime import datetime
from os import environ
from typing import Any


from sqlalchemy import MetaData, Table, Column, Integer, String, DateTime, select, insert, delete
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import Mapped, declarative_base


from starlite import Starlite, State, DTOFactory, Controller, Response, HTTPException
from starlite.handlers import get, post
from starlite.plugins.sql_alchemy import SQLAlchemyConfig, SQLAlchemyPlugin
from starlite.status_codes import HTTP_404_NOT_FOUND


# Define database connection credentials
db_host = environ.get("POSTGRES_HOST", "localhost")
db_user = environ.get("POSTGRES_USER", "postgres")
db_password = environ.get("POSTGRES_PASSWORD", "postgres_password")
db_name = environ.get("POSTGRES_DB", "staff")
sqlalchemy_config = SQLAlchemyConfig(
    connection_string="postgresql://{}:{}@{}/{}".format(
        db_user, db_password, db_host, db_name
    ),
    use_async_engine=False,
)
sqlalchemy_plugin = SQLAlchemyPlugin(config=sqlalchemy_config)
dto_factory = DTOFactory(plugins=[sqlalchemy_plugin])

# # Use Core method to describe db structure
# metadata = MetaData()
# employees_table = Table('employees', metadata,
#                         Column('id', Integer(), primary_key=True, autoincrement=True),
#                         Column('name', String(50), nullable=False, index=True),
#                         Column('post', String(10), nullable=False),
#                         Column('created_on', DateTime(), default=datetime.now),
#                         Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now))


Base = declarative_base()


class Employee(Base):
    __tablename__ = "employees"
    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String)
    post: Mapped[str] = Column(String)


CreateEmployeeDTO = dto_factory("CreateEmployeeDTO", Employee)


class EmployeeResponse(Response):
    def serializer(self, value: Any):
        if isinstance(value[0], Employee):
            return [
                {"id": record.id, "name": record.name, "post": record.post}
                for record in value
            ]
        return super().serializer(value)


async def on_startup(state: State) -> None:
    """Initialize database connection and store it into state item."""
    engine = create_async_engine(
        "postgresql+asyncpg://{}:{}@{}/{}".format(
            db_user, db_password, db_host, db_name
        ),
        echo=True,
    )
    # async with engine.begin() as conn:
    # await conn.run_sync(Base.metadata.drop_all)
    # await conn.run_sync(Base.metadata.create_all)
    # metadata.create_all(engine)
    state.engine = engine


async def on_shutdown(state: State) -> None:
    """Closes the db connection pool stored in the application State object."""
    if getattr(state, "engine", None):
        await state.engine.dispose()


class EmployeeController(Controller):
    """
    Manages employees info (retrieve from database etc).
    """
    path = "/employees"

    @get(path='/delete/')
    async def delete_employees(self, state: State) -> None:
        """Get employees list and return it."""
        async with state.engine.connect() as conn:
            await conn.execute(delete(Employee))
            await conn.commit()

    @get(name="employees_list", response_class=EmployeeResponse)
    async def employees_list(self, state: State) -> list[Employee]:
        """Get employees list and return it."""
        async with state.engine.connect() as conn:
            result = await conn.execute(select(Employee))
            if not result:
                raise HTTPException(
                    detail=f"No employees found", status_code=HTTP_404_NOT_FOUND
                )
            records_list = result.fetchall()
            # biuld JSON based on list of sqlalchemy.engine.row.Row objects
            employees = [
                 {"id": record.id, "name": record.name, "post": record.post}
                 for record in records_list
            ]
            return employees

    @get(path="/{employee_id:int}/", name="employee_details", response_class=EmployeeResponse)
    async def get_employee(self, employee_id: int, state: State) -> Employee:
        """Get an employee by its ID and return it.
        If it doesn't with that ID does not exist, return a 404 response
        """
        async with state.engine.connect() as conn:
            result = await conn.execute(select(Employee).where(Employee.id == employee_id))
            if not result:
                raise HTTPException(
                    detail=f"No employees found", status_code=HTTP_404_NOT_FOUND
                )
            records_list = result.fetchall()
            employees = [
                {"id": record.id, "name": record.name, "post": record.post}
                for record in records_list
            ]
            return employees

    @post()
    async def create_employee(self, data: CreateEmployeeDTO, state: State) -> Any:
        async with state.engine.connect() as conn:
            employee: Employee = data.to_model_instance()
            result = await conn.execute(insert(Employee).values(id=employee.id, name=employee.name, post=employee.post))
            await conn.commit()
            return employee



    # @patch(path="/{employee_id:str}/")
    # async def update_employee(self, data: Partial[Employee]) -> None:
    #     pass

    # @delete(path="/{employee_id:str}/")
    # async def delete_employee(self, data: Employee) -> None:
    #     pass


app = Starlite(
    route_handlers=[EmployeeController],
    on_startup=[on_startup],
    on_shutdown=[on_shutdown],
    plugins=[sqlalchemy_plugin],
)
