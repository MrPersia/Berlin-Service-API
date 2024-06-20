from typing import List
from model import Service, engine, initialize_database , check_if_table_exists
import controller
import uvicorn
from fastapi import FastAPI, HTTPException, Body
from sqlmodel import Field, Session, SQLModel, create_engine, select
from model import Service, get_all_service_titles, get_service_details, get_digital_services, get_services_by_office, get_all_form_links

# Initialize the database if not already initialized
initialize_database()

# Create an instance of the FastAPI app
app = FastAPI()

@app.get("/")
def test_root():
    return "Hi from da Mohsen 🙋🏻‍♂️"


@app.get("/Dienstleistungen")
def run_scraper():
    # Triggers a controller function
    controller.get_service()
    return "Scraping Successful"

@app.get("/saved-Dienstleistungen")
def get_Dienstleistungen_from_db():
    Service = controller.get_service_from_db()
    print(Service)
    return Service

#GET /ALL-SERVICES: GIBT DIE TITEL ALLER SERVICES, SOWIE IHRE ID ZURÜCK

@app.get("/all-services")
def get_all_services():
    return get_all_service_titles()

# GET /SERVICE/<SERVICE_ID>: GIBT DIE DETAILS ZU EINEM SERVICE ZURÜCK
@app.get("/service/{service_id}")
def get_service(service_id: int):
    service = get_service_details(service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service

#GET /ALL-SERVICES?DIGITAL-SERVICE=TRUE/FALSE: FILTER NACH ONLINE/ OFFLINE SERVICES
@app.get("/all-services/digital-service/{is_digital}")
def get_digital_services_endpoint(is_digital: bool):
    return get_digital_services(is_digital)

#GET /ALL-SERVICES?RESPONSIBLE-OFFICE=...: FILTER NACH ZUGEHÖRIGEM AMT
@app.get("/all-services/responsible-office/{office}")
def get_services_by_office_endpoint(office: str):
    return get_services_by_office(office)

#GET /ALL-FORMS: GIBT ALLE ADRESSEN VON FORMULAREN ZURÜCK
@app.get("/all-forms")
def get_all_forms():
    return get_all_form_links()

if __name__ == "__main__":
    # Anfang allen Übels
    run_scraper()
    uvicorn.run(app)
