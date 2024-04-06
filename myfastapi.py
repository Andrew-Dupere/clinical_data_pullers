from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, select, MetaData, Table
from typing import List
import arcturis as a

# Create FastAPI instance
app = FastAPI()

# MySQL Database Configuration
DATABASE_URL = a.DB  # Replace with your actual database URL
engine = create_engine(DATABASE_URL)
metadata = MetaData()
metadata.bind = engine

# Reflect the table schema
clinical_trials = Table('clinical_trials_test', metadata, autoload_with=engine)

# Function to search for a term in all columns
def search_term_in_all_columns(search_term: str):
    # Build the query
    query = select([clinical_trials]).where(
        clinical_trials.columns['Conditions'].like(f'%{search_term}%')
    )

    # Execute the query
    with engine.connect() as connection:
        result = connection.execute(query)
        data = [dict(row) for row in result]

    return data

# FastAPI endpoint to search for a term in all columns
#url = "http://localhost:8000/search/?search_term=Melanoma"

@app.get("/search/")
async def search_term_api(search_term: str):
    data = search_term_in_all_columns(search_term)
    if not data:
        raise HTTPException(status_code=404, detail="No matching rows found")
    
    return data
