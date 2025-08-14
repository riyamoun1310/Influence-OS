
from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

app = FastAPI(title="Influence-OS1 Backend")
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],  # In production, specify your frontend URL
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

# Ask AI endpoint (OpenAI or placeholder)
class AskRequest(BaseModel):
	question: str
	context: Optional[str] = None

@app.post("/ask")
def ask_ai(req: AskRequest = Body(...)):
	# If you have OpenAI API key configured, use it here
	openai_api_key = os.getenv("OPENAI_API_KEY")
	if openai_api_key:
		import openai
		openai.api_key = openai_api_key
		prompt = req.question
		if req.context:
			prompt = f"Context: {req.context}\nQuestion: {req.question}"
		try:
			response = openai.ChatCompletion.create(
				model="gpt-3.5-turbo",
				messages=[{"role": "user", "content": prompt}],
				max_tokens=200
			)
			answer = response['choices'][0]['message']['content']
			return {"answer": answer}
		except Exception as e:
			return {"error": str(e)}
	# If no OpenAI key, return a placeholder
	return {"answer": f"(Demo) You asked: '{req.question}' with context: '{req.context or ''}'"}

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


# Get user profile (real DB data)
@app.get("/profile")
def get_profile(email: str = Query(...)):
	user = get_user_by_email(email)
	if not user:
		raise HTTPException(status_code=404, detail="User not found")
	return {"profile": user.profile_data}

# Get all users (for admin/testing)
@app.get("/users")
def get_users():
	db = SessionLocal()
	users = db.query(User).all()
	db.close()
	return [{"email": u.email, "name": u.name, "profile_data": u.profile_data} for u in users]

# Get calendar entries for a user
@app.get("/calendar")
def get_calendar(email: str = Query(...)):
	db = SessionLocal()
	user = db.query(User).filter(User.email == email).first()
	if not user:
		db.close()
		raise HTTPException(status_code=404, detail="User not found")
	entries = db.query(CalendarEntry).filter(CalendarEntry.user_id == user.id).all()
	db.close()
	return [{
		"content": e.content,
		"scheduled_time": e.scheduled_time.isoformat() if e.scheduled_time else None,
		"status": e.status
	} for e in entries]

# Get analytics for a user
@app.get("/analytics")
def get_analytics(email: str = Query(...)):
	db = SessionLocal()
	user = db.query(User).filter(User.email == email).first()
	if not user:
		db.close()
		raise HTTPException(status_code=404, detail="User not found")
	analytics = db.query(Analytics).filter(Analytics.user_id == user.id).first()
	db.close()
	if not analytics:
		return {"posts": 0, "likes": 0, "comments": 0, "shares": 0}
	return {
		"posts": analytics.posts,
		"likes": analytics.likes,
		"comments": analytics.comments,
		"shares": analytics.shares
	}

# Schedule content (add to calendar)
@app.post("/schedule-content")
def schedule_content(req: ScheduleRequest):
	db = SessionLocal()
	user = db.query(User).filter(User.email == req.email).first()
	if not user:
		db.close()
		raise HTTPException(status_code=404, detail="User not found")
	scheduled_time = req.scheduled_time or datetime.utcnow()
	entry = CalendarEntry(user_id=user.id, content=req.content, scheduled_time=scheduled_time, status="scheduled")
	db.add(entry)
	db.commit()
	db.refresh(entry)
	db.close()
	return {"message": "Content scheduled.", "entry": {
		"content": entry.content,
		"scheduled_time": entry.scheduled_time.isoformat() if entry.scheduled_time else None,
		"status": entry.status
	}}

# Onboard user (create or update)
@app.post("/onboard")
def onboard_user(profile: UserProfile):
	create_or_update_user(profile)
	return {"message": f"Welcome, {profile.name}! Your profile is set up."}

# ...existing code for /onboard and /schedule-content endpoints...

# Paste here:
# Generate Article endpoint
@app.get("/generate-article")
def generate_article(email: str = Query(...)):
    user = get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "title": "How to Build Influence on LinkedIn",
        "content": f"This is a generated article for {user.name}. Start by optimizing your profile..."
    }

# Generate Carousel endpoint
@app.get("/generate-carousel")
def generate_carousel(email: str = Query(...)):
    user = get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "slides": [
            {"title": "Step 1", "content": "Optimize your LinkedIn profile."},
            {"title": "Step 2", "content": "Post regularly with value."},
            {"title": "Step 3", "content": f"Engage with your network, {user.name}."}
        ]
    }

# --- Added missing endpoints for frontend integration ---
@app.get("/generate-content")
def generate_content(email: str = Query(...)):
	user = get_user_by_email(email)
	if not user:
		raise HTTPException(status_code=404, detail="User not found")
	return {
		"content": f"Generated content for {user.name}. Post something valuable!"
	}

@app.get("/industry-news")
def industry_news(query: str = Query(...)):
	# Dummy news data
	return {
		"articles": [
			{"title": f"Latest in {query}", "summary": f"This is a summary about {query}."},
			{"title": f"{query} Trends", "summary": f"Trends in {query} for 2025."}
		]
	}

@app.post("/compliance-check")
def compliance_check():
	# Dummy compliance check
	return {"compliant": True, "details": "Content is compliant with guidelines."}

@app.get("/linkedin/login")
def linkedin_login():
	# Dummy LinkedIn login endpoint
	return {"message": "LinkedIn login placeholder. Implement OAuth here."}