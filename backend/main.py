# FastAPI and imports
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from typing import Optional
import os
import openai
import requests
from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, timedelta

app = FastAPI(title="Influence-OS1 Backend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class UserProfile(BaseModel):
    name: str
    email: str
    linkedin_url: str

class ScheduleRequest(BaseModel):
    email: str
    content: str
    scheduled_time: Optional[str] = None  # ISO format


# FastAPI and imports (move to top)

# FastAPI and imports
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
# Database setup
class UserProfile(BaseModel):
    name: str
    email: str
    linkedin_url: str
    tone: str
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import Optional
import os
import openai
import requests
# SQLAlchemy for PostgreSQL
from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# SQLAlchemy for PostgreSQL
from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/influenceos")
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

# DB-backed user functions
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




# Generate LinkedIn article
@app.get("/generate-article")
def generate_article(email: str = Query(...)):
    user = get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    profile = user.profile_data
    name = profile.get('name', 'Professional')
    summary = profile.get('summary') or ''
    prompt = f"""
    Write a detailed, professional LinkedIn article for {name} that showcases their expertise and achievements. 
    The article should be at least 400 words, include a strong introduction, 2-3 key sections, and a conclusion with a call to action. 
    {summary}
        question: str
        context: Optional[str] = None

        # Universal AI Q&A endpoint
        @app.post("/ask")
        def ask_anything(req: AskRequest):
            prompt = req.question
            if req.context:
                prompt = f"Context: {req.context}\nQuestion: {req.question}"
            # Uncomment for real OpenAI integration
            # response = openai.ChatCompletion.create(
            #     model="gpt-4",
            #     messages=[{"role": "user", "content": prompt}],
            #     max_tokens=512
            # )
            # return {"answer": response['choices'][0]['message']['content']}
            # Demo static answer
            return {"answer": f"[Sample AI answer for: {prompt}]"}
    """
    # Uncomment for real OpenAI integration
    # response = openai.ChatCompletion.create(
    #     model="gpt-4",
    #     messages=[{"role": "user", "content": prompt}],
    #     max_tokens=800
    # )
    # return {"article": response['choices'][0]['message']['content']}
    # Demo static article
    return {"article": f"[Sample LinkedIn Article for {name}]\n\nIntroduction...\nKey Section 1...\nKey Section 2...\nConclusion: Let's connect!"}

# Generate LinkedIn carousel (multi-slide post)
@app.get("/generate-carousel")
def generate_carousel(email: str = Query(...)):
    user = get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    profile = user.profile_data
    name = profile.get('name', 'Professional')
    summary = profile.get('summary') or ''
    prompt = f"""
    Create a LinkedIn carousel post for {name} with 5 slides. Each slide should have a catchy headline and a short, impactful message. 
    The carousel should highlight {name}'s skills, achievements, and value to employers. 
    {summary}
    """
    # Uncomment for real OpenAI integration
    # response = openai.ChatCompletion.create(
    #     model="gpt-4",
    #     messages=[{"role": "user", "content": prompt}],
    #     max_tokens=400
    # )
    # return {"carousel": response['choices'][0]['message']['content']}
    # Demo static carousel
    slides = [
        f"Slide 1: Meet {name}!",
        "Slide 2: My Top Skills",
        "Slide 3: Achievements",
        "Slide 4: What I Bring to the Table",
        "Slide 5: Let's Connect!"
    ]
    return {"carousel": slides}




# Industry research endpoint (NewsAPI)
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "your_newsapi_key")
NEWSAPI_URL = "https://newsapi.org/v2/top-headlines"

@app.get("/industry-news")
def industry_news(query: str = "AI", country: str = "in"):
    params = {
        "q": query,
        "country": country,
        "apiKey": NEWSAPI_KEY,
        "pageSize": 5
    }
    resp = requests.get(NEWSAPI_URL, params=params)
    if resp.status_code != 200:
        return {"error": "Failed to fetch news", "details": resp.json()}
    articles = resp.json().get("articles", [])
    return {"articles": articles}

# LinkedIn OAuth 2.0 integration (scaffold)
LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID", "your_linkedin_client_id")
LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET", "your_linkedin_client_secret")
LINKEDIN_REDIRECT_URI = os.getenv("LINKEDIN_REDIRECT_URI", "http://localhost:8000/linkedin/callback")
LINKEDIN_AUTH_URL = "https://www.linkedin.com/oauth/v2/authorization"
LINKEDIN_TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
LINKEDIN_PROFILE_URL = "https://api.linkedin.com/v2/me"
LINKEDIN_EMAIL_URL = "https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))"

# Step 1: Redirect user to LinkedIn for authorization
@app.get("/linkedin/login")
def linkedin_login():
    params = {
        "response_type": "code",
        "client_id": LINKEDIN_CLIENT_ID,
        "redirect_uri": LINKEDIN_REDIRECT_URI,
        "scope": "r_liteprofile r_emailaddress w_member_social"
    }
    url = f"{LINKEDIN_AUTH_URL}?" + "&".join([f"{k}={v}" for k, v in params.items()])
    return RedirectResponse(url)

# Step 2: LinkedIn callback to exchange code for access token
@app.get("/linkedin/callback")
def linkedin_callback(code: str):
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": LINKEDIN_REDIRECT_URI,
        "client_id": LINKEDIN_CLIENT_ID,
        "client_secret": LINKEDIN_CLIENT_SECRET
    }
    resp = requests.post(LINKEDIN_TOKEN_URL, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    token = resp.json().get("access_token")
    if not token:
        return {"error": "Failed to get access token", "details": resp.json()}
    # Fetch profile and email
    profile = requests.get(LINKEDIN_PROFILE_URL, headers={"Authorization": f"Bearer {token}"}).json()
    email = requests.get(LINKEDIN_EMAIL_URL, headers={"Authorization": f"Bearer {token}"}).json()
    return {"access_token": token, "profile": profile, "email": email}



# Content generation endpoint (convincing, hire-me tone)
def generate_convincing_content(profile):
    # This is a placeholder for OpenAI API call
    name = profile.get('name', 'Professional')
    industry = 'your industry'
    summary = profile.get('summary') or ''
    tone = profile.get('tone', 'convincing')
    # Prompt for OpenAI
    prompt = f"""
    Write a highly convincing LinkedIn post for {name} that will make companies want to hire them. 
    Use a confident, professional, and engaging tone. Highlight their skills, experience, and potential. 
    {summary}
    End with a strong call to action for recruiters and companies.
    """
    # Uncomment and configure this for real OpenAI integration
    # response = openai.ChatCompletion.create(
    #     model="gpt-4",
    #     messages=[{"role": "user", "content": prompt}],
    #     max_tokens=300
    # )
    # return response['choices'][0]['message']['content']
    # For demo, return a static sample
    return f"🚀 Hi LinkedIn! I'm {name}, passionate about making an impact in {industry}. With a proven track record and a drive for excellence, I'm ready to take on new challenges. If you're looking for someone who delivers results and brings fresh ideas, let's connect! #OpenToWork #HireMe"

@app.get("/generate-content")
def generate_content(email: str = Query(...)):
    user = get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    profile = user.profile_data
    content = generate_convincing_content(profile)
    return {"content": content}

# User profile model
class UserProfile(BaseModel):
    name: str
    email: str
    linkedin_url: str
    summary: Optional[str] = None
    tone: Optional[str] = "convincing"


# In-memory stores (for demo)
user_db = {}

# In-memory stores (for demo)
user_db = {}
content_calendar = []
analytics_db = {}
# Schedule content (add to calendar)

class ScheduleRequest(BaseModel):
    email: str
    content: str
    scheduled_time: Optional[str] = None  # ISO format

@app.post("/schedule-content")
def schedule_content(req: ScheduleRequest):
    scheduled_time = req.scheduled_time or (datetime.utcnow() + timedelta(hours=1)).isoformat()
    entry = {
        "email": req.email,
        "content": req.content,
        "scheduled_time": scheduled_time,
        "status": "scheduled"
    }
    content_calendar.append(entry)
    return {"message": "Content scheduled.", "entry": entry}

# DB-backed content calendar
@app.post("/schedule-content")
def schedule_content(req: ScheduleRequest):
    db = SessionLocal()
    user = db.query(User).filter(User.email == req.email).first()
    if not user:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")
    scheduled_time = req.scheduled_time or (datetime.utcnow() + timedelta(hours=1)).isoformat()
    entry = CalendarEntry(user_id=user.id, content=req.content, scheduled_time=scheduled_time, status="scheduled")
    db.add(entry)
    db.commit()
    db.refresh(entry)
    db.close()
    return {"message": "Content scheduled.", "entry": {
        "email": req.email,
        "content": req.content,
        "scheduled_time": scheduled_time,
        "status": "scheduled"
    }}

# Get content calendar
@app.get("/calendar/{email}")
def get_calendar(email: str):
    return [c for c in content_calendar if c["email"] == email]

# DB-backed get content calendar
@app.get("/calendar/{email}")
def get_calendar(email: str):
    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    if not user:
        db.close()
        return []
    entries = db.query(CalendarEntry).filter(CalendarEntry.user_id == user.id).all()
    db.close()
    return [{
        "content": e.content,
        "scheduled_time": e.scheduled_time.isoformat() if e.scheduled_time else None,
        "status": e.status
    } for e in entries]

# Analytics endpoint
@app.get("/analytics/{email}")
def get_analytics(email: str):
    return analytics_db.get(email, {"posts": 0, "likes": 0, "comments": 0, "shares": 0})

# DB-backed analytics
@app.get("/analytics/{email}")
def get_analytics(email: str):
    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    if not user:
        db.close()
        return {"posts": 0, "likes": 0, "comments": 0, "shares": 0}
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

# Placeholder for LinkedIn posting (to be implemented with LinkedIn API)
@app.post("/post-linkedin")
def post_linkedin(req: ScheduleRequest):
    # TODO: Integrate with LinkedIn API for real posting
    # For now, mark as posted and update analytics
    for entry in content_calendar:
        if entry["email"] == req.email and entry["content"] == req.content:
            entry["status"] = "posted"
    # Update analytics
    stats = analytics_db.setdefault(req.email, {"posts": 0, "likes": 0, "comments": 0, "shares": 0})
    stats["posts"] += 1
    return {"message": "Content posted to LinkedIn (simulated)."}

# DB-backed post to LinkedIn (simulated)
@app.post("/post-linkedin")
def post_linkedin(req: ScheduleRequest):
    db = SessionLocal()
    user = db.query(User).filter(User.email == req.email).first()
    if not user:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")
    # Mark calendar entry as posted
    entry = db.query(CalendarEntry).filter(CalendarEntry.user_id == user.id, CalendarEntry.content == req.content).first()
    if entry:
        entry.status = "posted"
    # Update analytics
    analytics = db.query(Analytics).filter(Analytics.user_id == user.id).first()
    if not analytics:
        analytics = Analytics(user_id=user.id, posts=1, likes=0, comments=0, shares=0)
        db.add(analytics)
    else:
        analytics.posts += 1
    db.commit()
    db.close()
    return {"message": "Content posted to LinkedIn (simulated)."}

# Advanced compliance check using OpenAI moderation and professional language filter
@app.post("/compliance-check")
def compliance_check(req: ScheduleRequest):
    flagged = False
    flagged_reason = []
    # OpenAI moderation API (if available)
    try:
        moderation = openai.Moderation.create(input=req.content)
        if moderation['results'][0]['flagged']:
            flagged = True
            flagged_reason.append("OpenAI moderation flagged content.")
    except Exception:
        pass  # If OpenAI moderation fails, continue with manual checks
    # Simple professional language filter
    unprofessional_words = ["hate", "stupid", "idiot", "fool", "unprofessional", "offensive"]
    for word in unprofessional_words:
        if word in req.content.lower():
            flagged = True
            flagged_reason.append(f"Contains unprofessional word: {word}")
    if not flagged:
        return {"compliant": True, "message": "Content is professional."}
    return {"compliant": False, "message": " ".join(flagged_reason) or "Content may need review for professionalism."}

@app.get("/")
def read_root():
    return {"message": "Influence-OS1 backend is running."}

# Onboard user (DB-backed)
@app.post("/onboard")
def onboard_user(profile: UserProfile):
    create_or_update_user(profile)
    return {"message": f"Welcome, {profile.name}! Your profile is set up for LinkedIn content automation."}

# LinkedIn integration placeholder
@app.get("/profile/{email}")
def get_profile(email: str):
    user = get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # TODO: Fetch and analyze LinkedIn profile using LinkedIn API
    return {"profile": user.profile_data, "analysis": "(Profile analysis will appear here)"}
