import asyncio
import asyncpg

# from asyncpg import connect,
from os import environ
from sqlalchemy import Column, Integer, String, select
from sqlalchemy.orm import Mapped, Session, declarative_base
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import create_async_engine

from starlite import State, Controller, DTOFactory, HTTPException, Starlite, get
from starlite.plugins.sql_alchemy import SQLAlchemyConfig, SQLAlchemyPlugin
from starlite.status_codes import HTTP_404_NOT_FOUND
from typing import Optional


Base = declarative_base()
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
# dto_factory = DTOFactory(plugins=[sqlalchemy_plugin])


class Employee(Base):
    __tablename__ = "employees"
    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String)
    post: Mapped[float] = Column(String)


async def on_startup(state: State) -> None:
    """Initialize database connection and store it into state item."""
    engine = create_async_engine(
        "postgresql+asyncpg://{}:{}@{}/{}".format(
            db_user, db_password, db_host, db_name
        ),
        poolclass=NullPool,
        echo=True,
    )
    # async with engine.begin() as conn:
    # await conn.run_sync(Base.metadata.drop_all)
    # await conn.run_sync(Base.metadata.create_all)
    state.engine = engine


async def on_shutdown(state: State) -> None:
    """Closes the db connection pool stored in the application State object."""
    if getattr(state, "engine", None):
        await state.engine.dispose()


class EmployeeController(Controller):
    """
    Manages employees info (retrieve from database etc).
    """
    @get(path="/employees/")
    async def employees_list(self, state: State) -> dict:
        """Get employees list and return it."""
        async with state.engine.connect() as conn:
            result = await conn.execute(select(Employee))
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

    @get(path="/employees/{employee_id:str}/")
    async def get_employee(self, employee_id: int, state: State) -> dict:
        """Get an employee by its ID and return it.
        If it doesn't with that ID does not exist, return a 404 response
        """
        """Get employees list and return it."""
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


app = Starlite(
    route_handlers=[EmployeeController],
    on_startup=[on_startup],
    on_shutdown=[on_shutdown],
    plugins=[sqlalchemy_plugin],
)
