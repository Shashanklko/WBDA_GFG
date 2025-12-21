from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine
from app.db.models import User, Agency
from app.core.security import get_password_hash
from app.db.models import Base
import pandas as pd
import numpy as np
import os
import random

def seed_users(db: Session):
    # Check if admin exists
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        admin_user = User(
            username="admin",
            hashed_password=get_password_hash("admin123"),
            role="admin"
        )
        db.add(admin_user)
        print("Created Admin user (admin/admin123)")

    # Create Agency
    agency = db.query(Agency).filter(Agency.name == "Clean Water Authority").first()
    if not agency:
        agency = Agency(
            name="Clean Water Authority",
            location="Metropolis",
            contact_info="contact@cleanwater.org"
        )
        db.add(agency)
        db.commit()
        db.refresh(agency)
        print("Created Agency 'Clean Water Authority'")

    # Create Agency User
    agency_user = db.query(User).filter(User.username == "agency").first()
    if not agency_user:
        agency_user = User(
            username="agency",
            hashed_password=get_password_hash("agency123"),
            role="agency",
            agency_id=agency.id
        )
        db.add(agency_user)
        print("Created Agency user (agency/agency123)")
    
    db.commit()

def generate_synthetic_data():
    num_rows = 1000
    regions = ["North", "South", "East", "West", "Central"]
    countries = ["Country A", "Country B", "Country C"]
    water_sources = ["River", "Well", "Lake", "Piped", "Spring"]
    treatment_methods = ["Chlorination", "Boiling", "Filtration", "None", "UV"]

    data = {
        "Country": [random.choice(countries) for _ in range(num_rows)],
        "Region": [random.choice(regions) for _ in range(num_rows)],
        "Year": [random.randint(2018, 2023) for _ in range(num_rows)],
        "Water Source Type": [random.choice(water_sources) for _ in range(num_rows)],
        "Water Treatment Method": [random.choice(treatment_methods) for _ in range(num_rows)],
        "Contaminant Level (ppm)": np.random.uniform(0, 100, num_rows),
        "pH Level": np.random.uniform(5, 9, num_rows),
        "Turbidity (NTU)": np.random.uniform(0, 10, num_rows),
        "Dissolved Oxygen (mg/L)": np.random.uniform(2, 12, num_rows),
        "Nitrate Level (mg/L)": np.random.uniform(0, 50, num_rows),
        "Lead Concentration (µg/L)": np.random.uniform(0, 20, num_rows),
        "Bacteria Count (CFU/mL)": np.random.randint(0, 500, num_rows),
        "Diarrheal Cases": np.random.randint(0, 100, num_rows),
        "Cholera Cases": np.random.randint(0, 20, num_rows),
        "Typhoid Cases": np.random.randint(0, 30, num_rows),
        "Infant Mortality Rate": np.random.uniform(0, 50, num_rows),
        "Access to Clean Water (%)": np.random.uniform(40, 100, num_rows),
        "Sanitation Coverage (%)": np.random.uniform(30, 100, num_rows),
        "GDP per Capita": np.random.uniform(1000, 20000, num_rows),
        "Healthcare Access Index": np.random.uniform(0, 100, num_rows),
        "Urbanization Rate": np.random.uniform(10, 90, num_rows),
        "Rainfall": np.random.uniform(500, 3000, num_rows),
        "Temperature": np.random.uniform(10, 40, num_rows),
        "Population Density": np.random.uniform(10, 5000, num_rows),
    }
    
    df = pd.DataFrame(data)
    
    # Introduce some correlations for ML to find
    # High Bacteria -> High Disease
    df["Diarrheal Cases"] += (df["Bacteria Count (CFU/mL)"] * 0.1).astype(int)
    
    # Good infrastructure -> Low Disease
    df["Diarrheal Cases"] -= (df["Access to Clean Water (%)"] * 0.2).astype(int)
    df["Diarrheal Cases"] = df["Diarrheal Cases"].clip(lower=0)

    os.makedirs("data", exist_ok=True)
    df.to_csv("data/water_quality_dataset.csv", index=False)
    print("Generated synthetic dataset at data/water_quality_dataset.csv")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        print("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        seed_users(db)
        generate_synthetic_data()
    finally:
        db.close()
