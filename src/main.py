from datetime import datetime
from os import environ
from typing import Any


from sqlalchemy import Column, Integer, String, DateTime, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import Mapped, declarative_base
from sqlalchemy.orm import sessionmaker


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
        poolclass=NullPool,
        echo=True,
    )
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    state.engine = engine
    state.session = async_session()
    state.session.begin()


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
        result = await state.session.execute(select(Employee))
        if not result:
            raise HTTPException(
                detail=f"No employees found", status_code=HTTP_404_NOT_FOUND
            )
        records_list = result.fetchall()
        return records_list

    @get(path="/{employee_id:int}/", name="employee_details", response_class=EmployeeResponse)
    async def get_employee(self, employee_id: int, state: State) -> Employee:
        """Get an employee by its ID and return it.
        If it doesn't exist, return a 404 response
        """
        result = await state.session.execute(select(Employee).where(Employee.id == employee_id))
        records_list = result.first()
        if not records_list:
            raise HTTPException(
                detail=f"No employees found", status_code=HTTP_404_NOT_FOUND
            )
        return records_list

    @post()
    async def create_employee(self, data: CreateEmployeeDTO, state: State) -> Employee:
        employee: Employee = data.to_model_instance()
        state.session.add(employee)
        await state.session.commit()
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
