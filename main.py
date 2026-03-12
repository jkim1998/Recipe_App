from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv


load_dotenv()

pw = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")
DATABASE_URL = f'mysql+pymysql://root:{pw}@localhost:3306/{db_name}'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class RecipeModel(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    minutes = Column(Integer)
    steps = Column(Text)
    description = Column(Text)
    ingredients = Column(Text)

class RecipeSchema(BaseModel):
    id: int
    name: str
    minutes: int
    description: Optional[str]
    
    class Config:
        from_attributes = True

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/recipes/{recipe_id}", response_model=RecipeSchema)
def read_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(RecipeModel).filter(RecipeModel.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

# curl.exe -X POST -H "Content-Type: application/json" "http://127.0.0.1:8000/items?item=apple"
# curl.exe -X GET http://127.0.0.1:8000/items/0

#uvicorn main:app --reload