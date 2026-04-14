DeployHub – Cat API Integration Service
A Flask-based web service that integrates an external API and a database to fetch, display, and store cat images.

    Team
Grace Rosemary Gaffney 124386911
Elle Mcmanus 124448216
Sarah O Sullivan 124442342

    Repository
git clone https://github.com/GracexGaffneyyyy/FlaskProject15
cd FlaskProject15

    Live Deployment
https://flaskproject15.onrender.com

    Project Overview
This application integrates:
External API: TheCatAPI
Database: SQLite (local development)
It provides:
Web interface (HTML + Flask)
JSON API endpoints

    Tech Stack
Python 3.11
Flask
SQLAlchemy
Requests
Docker
Gunicorn
GitHub Actions (CI/CD)

     Features
Fetch random cat images
Save images to database
View saved images
API endpoint (/api/cat)
Health and status endpoints
Dockerised deployment

    Setup
Install dependencies:
pip install -r requirements.txt
Create .env file:
CAT_API_KEY= live_nd5ftUYkwJRLVWcOyHHUAK9tzvrqCTqi5APyWJBCIti0jxtwEa6Q06uBcv5twr7P
ENVIRONMENT=development
PORT=5000

    Run the App
python app.py
Open:
http://127.0.0.1:5000

    Docker
docker build -t deployhub .
docker run -p 5000:5000 --env-file .env deployhub

    API Endpoints
/api/cat → returns random cat image (JSON)
/health → health check
/ready → readiness
/status → diagnostics

    UI Pages
/ → Home
/cat → View cat
/saved → Saved cats

    Observability
/health → service status
/ready → readiness
/status → uptime, DB status, configuration

    CI/CD
This project is configured for GitHub Actions.

    CI
Runs on push and pull requests
Installs dependencies
Builds Docker image

    CD
Deploys to Render from main branch


