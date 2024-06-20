# Determine the data to be extracted
# Datatype shall be a class variable

from typing import Optional, List
import fastapi 
from sqlalchemy import inspect
from sqlmodel import Field, Session, SQLModel, create_engine, select

engine = create_engine("sqlite:///service.db")


def initialize_database():
    # We have Service as an SQLModel defined, we need to create that metadate to do operations on it
    SQLModel.metadata.create_all(engine)


db_already_initialized = False


def check_if_table_exists():
    global db_already_initialized
    if not db_already_initialized:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        if not "service" in tables:
            initialize_database()
            print("Database initialized")
            db_already_initialized = True


class Service(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    is_digital: bool
    responsible_office: Optional[str] = None
    form_link: Optional[str] = None

    def __str__(self):
        return f"Title: {self.title}\ndescription: {self.description}\nis_digital: {self.is_digital}\nresponsible_office: {self.responsible_office}\nform_link: {self.form_link} \n"

def create(data):
    check_if_table_exists()

    with Session(engine) as session:
        session.add(data)
        session.commit()

def get_all_service_titles() -> List[dict]:
    with Session(engine) as session:
        services = session.exec(select(Service))
        result = [{"id": service.id, "title": service.title} for service in services]
        return result


def get_service_details(service_id: int) -> Optional[Service]:
    check_if_table_exists()
    with Session(engine) as session:
        statement = select(Service).where(Service.id == service_id)
        result = session.exec(statement).first()
        return result


def get_digital_services(is_digital: bool) -> List[dict]:
    with Session(engine) as session:
        statement = select(Service).where(Service.is_digital == is_digital)
        result = session.exec(statement).all()
        return [service.dict() for service in result]

def get_services_by_office(office: str) -> List[dict]:
    with Session(engine) as session:
        statement = select(Service).where(Service.responsible_office == office)
        result = session.exec(statement).all()
        return [service.dict() for service in result]


def get_all_form_links() -> List[str]:
    with Session(engine) as session:
        services = session.exec(select(Service)).all()
        result = [service.form_link for service in services if service.form_link is not None]
        return result

    
def get_all_services() -> List[dict]:
    with Session(engine) as session:
        services = session.exec(select(Service)).all()
        result = [{"id": service.id, "title": service.title} for service in services]
        return result