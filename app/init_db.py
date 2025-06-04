import requests
from sqlalchemy.orm import Session
from . import models, auth
from .database import engine as default_engine, SessionLocal as DefaultSessionLocal

def init_db(engine=None, session_factory=None):
    # Use provided engine/session_factory or fall back to defaults
    engine = engine or default_engine
    session_factory = session_factory or DefaultSessionLocal

    # Create tables
    models.Base.metadata.create_all(bind=engine)
    
    # Get sample data from JSONPlaceholder
    response = requests.get("https://jsonplaceholder.typicode.com/users")
    users_data = response.json()
    
    db = session_factory()
    try:
        # Check if we already have users
        if db.query(models.User).first():
            return
        
        # Create users with their related data
        for user_data in users_data:
            # Create user
            db_user = models.User(
                name=user_data["name"],
                username=user_data["username"],
                email=user_data["email"],
                password_hash=auth.get_password_hash("password123"),  # Default password
                phone=user_data["phone"],
                website=user_data["website"]
            )
            db.add(db_user)
            db.flush()
            
            # Create address
            address_data = user_data["address"]
            address = models.Address(
                street=address_data["street"],
                suite=address_data["suite"],
                city=address_data["city"],
                zipcode=address_data["zipcode"],
                user_id=db_user.id
            )
            db.add(address)
            db.flush()
            
            # Create geo
            geo_data = address_data["geo"]
            geo = models.Geo(
                lat=geo_data["lat"],
                lng=geo_data["lng"],
                address_id=address.id
            )
            db.add(geo)
            
            # Create company
            company_data = user_data["company"]
            company = models.Company(
                name=company_data["name"],
                catchPhrase=company_data["catchPhrase"],
                bs=company_data["bs"],
                user_id=db_user.id
            )
            db.add(company)
        
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    init_db() 