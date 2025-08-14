# Influence-OS1 - LinkedIn Personal Branding AI Agent

## Project Summary
Influence-OS1 is an autonomous AI agent that researches, creates, and posts personal branding content for LinkedIn. It analyzes user profiles, generates engaging content, schedules and posts automatically, and tracks engagement analytics—all with a professional, convincing tone to help users get hired.

## Project Structure
- `backend/` - FastAPI backend (Python)
- `frontend/` - Next.js frontend (React)
- `db/` - Database setup (PostgreSQL)

## Features
- User profile analysis
- Industry research
- Content strategy & generation
- Engagement optimization
- Performance analytics
- Automated posting
- Compliance & ethics

## Documentation & Deliverables
- [API Documentation](backend/openapi_docs.md)
- [User Guide](USER_GUIDE.md)
- [Deployment Instructions](DEPLOYMENT.md)
- [Technical Report Template](TECHNICAL_REPORT_TEMPLATE.md)


## Quick Start
1. See [Deployment Instructions](DEPLOYMENT.md) for setup and running locally or with Docker.
2. Use the onboarding page to set up your profile.
3. Access the dashboard, content calendar, and analytics from the frontend.

## Enabling Real OpenAI & LinkedIn API Keys
1. Copy `backend/.env.example` to `backend/.env`.
2. Add your real OpenAI API key, LinkedIn Client ID, and LinkedIn Client Secret to the `.env` file:
	- `OPENAI_API_KEY=sk-...`
	- `LINKEDIN_CLIENT_ID=...`
	- `LINKEDIN_CLIENT_SECRET=...`
3. Restart the backend server for changes to take effect.

## Submission Checklist
- [x] Working web application with user dashboard
- [x] Clean, documented source code (GitHub-ready)
- [x] Comprehensive API documentation
- [x] User guide and technical report
- [x] Content engagement and system performance analytics
- [x] Deployment instructions

For any issues, see the documentation or contact the maintainer.
