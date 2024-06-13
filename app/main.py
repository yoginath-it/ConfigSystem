from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, database, crud
from typing import List
from sqlalchemy.exc import NoResultFound

app = FastAPI()

# Initialize database
database.init_db()

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/create_configuration", response_model=schemas.Configuration)
def create_configuration(configuration: schemas.ConfigurationCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_configuration(db=db, configuration=configuration)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/configuration/{country_code}/{business_name}", response_model=schemas.Configuration)
def get_configuration_api(country_code: str, business_name: str, db: Session = Depends(get_db)):
    try:
        configuration = crud.get_configuration(db, country_code, business_name)
        if configuration is None:
            raise HTTPException(status_code=404, detail=f"Configuration not found for country code {country_code} and business name {business_name}")
        return configuration
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"Configuration not found for country code {country_code} and business name {business_name}")

@app.get("/get_configurations_by_country/{country_code}", response_model=list[schemas.Configuration])
def get_configurations_by_country_api(country_code: str, db: Session = Depends(get_db)):
    configurations = crud.get_configurations_by_country(db, country_code)
    if not configurations:
        raise HTTPException(status_code=404, detail=f"Configurations for country code {country_code} not found")
    return configurations

@app.post("/update_configuration/{country_code}/{business_name}", response_model=schemas.Configuration)
def update_configuration(
    country_code: str,
    business_name: str,
    configuration: schemas.ConfigurationCreate,
    db: Session = Depends(get_db)
):
    try:
        updated_configuration = crud.update_configuration(
            db=db,
            country_code=country_code,
            business_name=business_name,
            configuration=configuration
        )
        return updated_configuration
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/delete_configuration/{country_code}/{business_name}", response_model=schemas.Configuration)
def delete_configuration(country_code: str, business_name: str, db: Session = Depends(get_db)):
    try:
        return crud.delete_configuration(db=db, country_code=country_code, business_name=business_name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/delete_configurations/{country_code}", response_model=List[schemas.Configuration])
def delete_configurations_by_country(country_code: str, db: Session = Depends(get_db)):
    try:
        return crud.delete_configurations_by_country(db=db, country_code=country_code)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

