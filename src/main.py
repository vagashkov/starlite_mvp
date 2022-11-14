import asyncio

# from asyncpg import connect,
from os import environ
from sqlalchemy import Column, Float, Integer, String, select
from sqlalchemy.orm import Mapped, Session, declarative_base
from starlite import Controller, DTOFactory, HTTPException, Starlite, get
from starlite.plugins.sql_alchemy import SQLAlchemyConfig, SQLAlchemyPlugin
from starlite.status_codes import HTTP_404_NOT_FOUND
from typing import cast, Optional


Base = declarative_base()
db_host = environ.get('POSTGRES_HOST', 'localhost')

sqlalchemy_config = SQLAlchemyConfig(
    connection_string="postgresql://postgres:postgres_password@{}/staff".format(db_host),
    use_async_engine=False,
)
sqlalchemy_plugin = SQLAlchemyPlugin(config=sqlalchemy_config)
dto_factory = DTOFactory(plugins=[sqlalchemy_plugin])


class Employee(Base):
    __tablename__ = "employees"
    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String)
    post: Mapped[float] = Column(String)


def on_startup() -> None:
    """Initialize the database."""
    Base.metadata.create_all(sqlalchemy_config.engine)


class EmployeeController(Controller):
    """
    Manages employees info (retrieve from database etc).
    """

    @get(path="/employees/")
    def employees_list(self, db_session: Session) -> dict[str, str]:
        """Get a company by its ID and return it.
        If a company with that ID does not exist, return a 404 response
        """
        employees: Optional[Employee] = db_session.scalars(select(Employee)).all()
        if not employees:
            raise HTTPException(
                detail=f"No employees found", status_code=HTTP_404_NOT_FOUND
            )
        return employees

    @get(path="/employees/{employee_id:int}/")
    def get_employee(self, employee_id: str, db_session: Session) -> Employee:
        """Get an employee by its ID and return it.
        If it doesn't with that ID does not exist, return a 404 response
        """
        employee: Optional[Employee] = db_session.scalars(
            select(Employee).where(Employee.id == employee_id)
        ).one_or_none()
        if not employee:
            raise HTTPException(
                detail=f"Company with ID {employee_id} not found",
                status_code=HTTP_404_NOT_FOUND,
            )
        return employee


app = Starlite(
    route_handlers=[EmployeeController],
    on_startup=[on_startup],
    plugins=[sqlalchemy_plugin],
)
