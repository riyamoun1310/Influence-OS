# Influence OS API Documentation

## Base URL
`http://localhost:8000/`

## Endpoints

### 1. Onboard User
- **POST** `/onboard`
- **Body:**
  ```json
  {
    "name": "riya",
    "email": "riyamoun1310@gmail.com",
    "linkedin_url": "https://www.linkedin.com/in/riya-moun-209449284",
    "tone": "convincing"
  }
  ```
- **Response:** `{ "message": "Welcome, riya! Your profile is set up for LinkedIn content automation." }`

### 2. Get User Profile & Analysis
- **GET** `/profile/{email}`
- **Response:** `{ "profile": { ... }, "analysis": "..." }`

### 3. Generate Convincing Content
- **GET** `/generate-content?email={email}`
- **Response:** `{ "content": "..." }`

### 4. Schedule Content
- **POST** `/schedule-content`
- **Body:**
  ```json
  {
    "email": "riyamoun1310@gmail.com",
    "content": "...",
    "scheduled_time": "2025-08-13T10:00:00Z" // optional
  }
  ```
- **Response:** `{ "message": "Content scheduled.", "entry": { ... } }`

### 5. Get Content Calendar
- **GET** `/calendar/{email}`
- **Response:** `[ ... ]`

### 6. Post to LinkedIn (Simulated)
- **POST** `/post-linkedin`
- **Body:** Same as schedule-content
- **Response:** `{ "message": "Content posted to LinkedIn (simulated)." }`

### 7. Analytics
- **GET** `/analytics/{email}`
- **Response:** `{ "posts": 0, "likes": 0, "comments": 0, "shares": 0 }`

### 8. Compliance Check
- **POST** `/compliance-check`
- **Body:** Same as schedule-content
- **Response:** `{ "compliant": true, "message": "Content is professional." }`

---

For full OpenAPI docs, run the backend and visit `/docs` in your browser.
