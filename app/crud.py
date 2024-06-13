from sqlalchemy.orm import Session
from . import models, schemas
from .country_templates import validate_configuration
from sqlalchemy.exc import SQLAlchemyError

def get_configuration(db: Session, country_code: str, business_name: str):
    try:
        return db.query(models.Configuration).filter(
            models.Configuration.country_code == country_code,
            models.Configuration.business_name == business_name
        ).first()
    except SQLAlchemyError as e:
        raise ValueError(f"Error fetching configuration: {str(e)}")

def create_configuration(db: Session, configuration: schemas.ConfigurationCreate):
    validate_configuration(configuration.country_code, configuration.data)
    db_configuration = get_configuration(db, configuration.country_code, configuration.business_name)
    if db_configuration:
        raise ValueError(f"Configuration for country code {configuration.country_code} and business name {configuration.business_name} already exists.")
    db_configuration = models.Configuration(**configuration.dict())
    db.add(db_configuration)
    db.commit()
    db.refresh(db_configuration)
    return db_configuration

def update_configuration(db: Session, country_code: str, business_name: str, configuration: schemas.ConfigurationCreate):
    db_configuration = get_configuration(db, country_code, business_name)
    if not db_configuration:
        raise ValueError("Configuration not found")
    validate_configuration(configuration.country_code, configuration.data)
    
    for key, value in configuration.dict().items():
        setattr(db_configuration, key, value)
    
    db.commit()
    db.refresh(db_configuration)
    return db_configuration

def delete_configuration(db: Session, country_code: str, business_name: str):
    db_configuration = get_configuration(db, country_code, business_name)
    if not db_configuration:
        raise ValueError("Configuration not found")

    db.delete(db_configuration)
    db.commit()
    return db_configuration

def get_configurations_by_country(db: Session, country_code: str):
    return db.query(models.Configuration).filter(models.Configuration.country_code == country_code).all()
