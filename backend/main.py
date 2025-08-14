
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# FastAPI app setup
app = FastAPI(title="Influence-OS1 Backend")
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],  # In production, specify your frontend URL
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

# Pydantic models
class UserProfile(BaseModel):
	name: str
	email: str
	linkedin_url: str
	tone: Optional[str] = None

class ScheduleRequest(BaseModel):
	email: str
	content: str
	scheduled_time: Optional[str] = None  # ISO format

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
	__tablename__ = "users"
	id = Column(Integer, primary_key=True, index=True)
	linkedin_id = Column(String, unique=True, index=True, nullable=True)
	name = Column(String)
	email = Column(String, unique=True, index=True)
	profile_data = Column(JSON)
	created_at = Column(DateTime, default=datetime.utcnow)
	calendar = relationship("CalendarEntry", back_populates="user")
	analytics = relationship("Analytics", back_populates="user")

class CalendarEntry(Base):
	__tablename__ = "calendar"
	id = Column(Integer, primary_key=True, index=True)
	user_id = Column(Integer, ForeignKey('users.id'))
	content = Column(Text)
	scheduled_time = Column(DateTime)
	status = Column(String)
	user = relationship("User", back_populates="calendar")

class Analytics(Base):
	__tablename__ = "analytics"
	id = Column(Integer, primary_key=True, index=True)
	user_id = Column(Integer, ForeignKey('users.id'))
	posts = Column(Integer, default=0)
	likes = Column(Integer, default=0)
	comments = Column(Integer, default=0)
	shares = Column(Integer, default=0)
	user = relationship("User", back_populates="analytics")

# Create tables if not exist
Base.metadata.create_all(bind=engine)

# Utility functions
def get_user_by_email(email):
	db = SessionLocal()
	user = db.query(User).filter(User.email == email).first()
	db.close()
	return user

def create_or_update_user(profile):
	db = SessionLocal()
	user = db.query(User).filter(User.email == profile.email).first()
	if not user:
		user = User(name=profile.name, email=profile.email, profile_data=profile.dict())
		db.add(user)
	else:
		user.name = profile.name
		user.profile_data = profile.dict()
	db.commit()
	db.close()

# Example endpoint: Generate LinkedIn article
@app.get("/generate-article")
def generate_article(email: str = Query(...)):
	user = get_user_by_email(email)
	if not user:
		raise HTTPException(status_code=404, detail="User not found")
	profile = user.profile_data
	name = profile.get('name', 'Professional')
	summary = profile.get('summary') or ''
	return {"article": f"[Sample LinkedIn Article for {name}]\n\nIntroduction...\nKey Section 1...\nKey Section 2...\nConclusion: Let's connect!"}

# Example endpoint: Generate LinkedIn carousel
@app.get("/generate-carousel")
def generate_carousel(email: str = Query(...)):
	user = get_user_by_email(email)
	if not user:
		raise HTTPException(status_code=404, detail="User not found")
	profile = user.profile_data
	name = profile.get('name', 'Professional')
	return {"carousel": [f"Slide {i+1}: ..." for i in range(5)]}
