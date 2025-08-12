# Influence OS Deployment Instructions

## Prerequisites
- Python 3.8+
- Node.js 18+
- PostgreSQL (optional, for production)
- Docker (optional, for containerized deployment)

## Local Setup

### 1. Backend
- Navigate to `backend/`
- Create a `.env` file from `.env.example` and fill in your API keys
- Install dependencies:
  ```sh
  pip install -r requirements.txt
  ```
- Start the server:
  ```sh
  uvicorn main:app --reload
  ```

### 2. Frontend
- Navigate to `frontend/`
- Install dependencies:
  ```sh
  npm install
  ```
- Start the dev server:
  ```sh
  npm run dev
  ```

### 3. Database
- (Optional) Run the SQL in `db/init.sql` to set up PostgreSQL

## Docker Deployment
- Build and run containers using Docker Compose (add a `docker-compose.yml` as needed)

## Production
- Set environment variables securely
- Use a production server (e.g., Gunicorn, Nginx, Vercel for frontend)

---

For any issues, refer to the README or contact the maintainer.
