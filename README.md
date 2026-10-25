# MediPilot

**Healthcare, thoughtfully coordinated.**

MediPilot is a conversational healthcare appointment-scheduling application built with React, FastAPI, and a LangGraph workflow. It guides a user through appointment details over multiple messages and includes an authenticated administration area for validating and importing doctor-directory data.

> **Project status:** This is a development/portfolio project, not a production clinical system. Review its security, privacy, reliability, and operational requirements before using it with real patient information.

## Features

- **Conversational scheduling:** Send natural-language appointment requests through a chat interface.
- **Multi-turn workflow:** Continue scheduling conversations with a persistent `thread_id`.
- **Scheduling context:** The agent can collect missing details and return structured status and execution-trace information.
- **Conversation state:** Retrieve the current scheduling state for a conversation.
- **Doctor directory:** View doctor records and summary information through the administration area.
- **Validated JSON import:** Preview and validate a doctor JSON file before explicitly importing it.
- **Protected administration:** Admin login uses configured credentials and signed bearer tokens.
- **Responsive interface:** A healthcare-focused workspace for scheduling and doctor-directory management.
- **Local and containerized development:** Run the frontend and backend separately or with Docker Compose.

Features depend on the workflow and configuration in the source code. MediPilot does not replace clinical judgement or emergency services.

## Technology Stack

| Area | Technologies |
| --- | --- |
| Frontend | React, Vite, JavaScript, CSS, Lucide React |
| Backend API | Python, FastAPI, Uvicorn, Pydantic |
| Agent workflow | LangGraph, LangChain |
| Language model | Groq integration, configured with `GROQ_API_KEY` |
| Database | SQLite, SQLAlchemy |
| Workflow persistence | LangGraph SQLite checkpoint integration |
| Validation | pytest |
| Containers | Docker, Docker Compose |

## Architecture

```text
Browser
  |
  v
React + Vite frontend
  |
  | JSON over HTTP
  v
FastAPI backend
  |-- Conversational scheduling endpoint
  |-- LangGraph scheduling workflow
  |-- Conversation-state retrieval
  |-- Admin authentication
  |-- Doctor JSON validation and import
  |
  +--> SQLite database and workflow checkpoint storage
```

The workflow implementation lives primarily in `backend/app/graph.py`, with API routes in `backend/app/api.py`, data models in `backend/app/models.py`, and database setup in `backend/app/database.py`.

## Project Structure

```text
MediPilot/
├── backend/
│   ├── app/
│   │   ├── api.py              # FastAPI routes and admin authentication
│   │   ├── checkpointer.py     # LangGraph checkpoint setup
│   │   ├── config.py           # Groq model configuration
│   │   ├── database.py         # SQLAlchemy database setup
│   │   ├── doctor_import.py    # Doctor JSON validation and import
│   │   ├── graph.py            # Scheduling workflow
│   │   ├── models.py           # Database models
│   │   ├── state.py            # Workflow state
│   │   └── tools.py            # Scheduling tools
│   └── tests/                  # Backend tests
├── data/
│   └── doctors.json            # Doctor directory source data
├── frontend/
│   ├── public/                 # Favicon and public assets
│   └── src/
│       ├── services/api.js     # Frontend API calls
│       ├── App.jsx             # Main scheduling/admin interface
│       ├── App.css             # MediPilot design system
│       └── main.jsx            # React entry point
├── notebooks/
│   └── scheduling_demo.ipynb
├── .env.example
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Prerequisites

For local development:

- Python 3.11 (matches the backend Docker image) and `pip`.
- Node.js compatible with the Vite version in `frontend/package.json`, and npm.
- A Groq API key if the configured scheduling workflow calls the Groq model.
- Docker Desktop, if using Docker Compose.

## Configuration

Create a local environment file from the example.

**Windows PowerShell**
```powershell
Copy-Item .env.example .env
```

**macOS / Linux**
```bash
cp .env.example .env
```

Update the values in `.env`:

```dotenv
GROQ_API_KEY=your_groq_api_key
ADMIN_USERNAME=admin
ADMIN_PASSWORD=replace-with-a-long-unique-password
ADMIN_SECRET_KEY=replace-with-a-random-secret-at-least-32-characters-long
FRONTEND_URL=http://localhost:5173,http://127.0.0.1:5173
```

| Variable | Purpose |
| --- | --- |
| `GROQ_API_KEY` | API key used by the configured Groq model integration. |
| `ADMIN_USERNAME` | Username accepted by the admin login endpoint. |
| `ADMIN_PASSWORD` | Password accepted by the admin login endpoint. Use a unique secret. |
| `ADMIN_SECRET_KEY` | Secret used to sign admin bearer tokens. Use a random value of at least 32 characters. |
| `FRONTEND_URL` | Comma-separated frontend origins allowed by the backend CORS configuration. |

Do not commit `.env` or expose credentials in frontend variables. Values prefixed with `VITE_` are bundled into browser-accessible code and must never contain server secrets.

## Run Locally

Run commands from the repository root unless a step specifies the `frontend` directory.

### 1. Set up the backend

**Windows PowerShell**
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn backend.app.api:app --reload
```

**macOS / Linux**
```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn backend.app.api:app --reload
```

The API is available at `http://127.0.0.1:8000`. Interactive API documentation is available at `http://127.0.0.1:8000/docs`; the health endpoint is `http://127.0.0.1:8000/health`.

Ensure the environment variables are configured before using features that require Groq or administrator authentication.

### 2. Set up the frontend

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL printed by Vite, normally `http://localhost:5173`.

If the backend is running on another host or port, set `VITE_API_URL` in the frontend environment before starting/building the frontend. Leave it empty for the same-origin/local arrangement where appropriate.

### 3. Build the frontend

```bash
cd frontend
npm run build
```

To run the production build locally:

```bash
npm run preview
```

## Run with Docker Compose

Create and configure `.env` in the project root first, then run:

```bash
docker compose up --build
```

The frontend is exposed on `http://localhost:8080`. The backend is available internally to the Compose network and includes a `/health` check. To stop the services:

```bash
docker compose down
```

To also remove the named database volume, use `docker compose down -v` only if you intentionally want to delete persisted local data.

## API Overview

The API schema exposed by the running version at `/docs` is the source of truth for request and response details.

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/` | Service status |
| `GET` | `/health` | Health check |
| `POST` | `/api/v1/schedule` | Submit a conversational scheduling message |
| `GET` | `/api/v1/conversations/{thread_id}` | Retrieve conversation state |
| `GET` | `/api/v1/conversations/{thread_id}/debug` | Retrieve conversation debug state |
| `POST` | `/api/v1/admin/login` | Authenticate an administrator |
| `GET` | `/api/v1/admin/session` | Check the current admin session |
| `GET` | `/api/v1/admin/doctors` | List doctor records |
| `GET` | `/api/v1/admin/doctors/summary` | Retrieve doctor-directory summary |
| `POST` | `/api/v1/admin/doctors/preview` | Validate and preview a doctor JSON upload |
| `POST` | `/api/v1/admin/doctors/initialize` | Import validated doctor records |
| `POST` | `/api/v1/admin/doctors/reset` | Reset doctor-directory data and related records |

Scheduling requests use a JSON body with `query` and `thread_id`. For example:

```json
{
  "query": "I would like to book an appointment",
  "thread_id": "demo-session-001"
}
```

Continue a multi-turn conversation by reusing the same `thread_id`. Consult `/docs` for exact schemas.

## Doctor Directory Import

The admin workflow validates a JSON file before import.

1. Sign in using credentials configured in the backend environment.
2. Choose a `.json` file no larger than 2 MB.
3. Select **Validate and preview** to inspect validation results.
4. Review the previewed records.
5. Explicitly choose **Initialize database** to import.

Previewing does not write the records to the database. Import behavior and required fields are defined in `backend/app/doctor_import.py`. The reset action is destructive: it removes doctors, availability slots, and appointments according to the backend implementation. Review the confirmation carefully and maintain backups.

## Deployment Notes

The repository includes Dockerfiles and a Docker Compose configuration. A cloud deployment must be configured for its own frontend origin, backend URL, secrets, and persistent database storage.

- Set `FRONTEND_URL` to the exact deployed frontend origin(s), comma-separated if needed.
- Configure `VITE_API_URL` to the deployed backend base URL when frontend and backend are hosted separately.
- Keep administrator credentials and API keys in the hosting provider's server-side environment settings.
- SQLite files on ephemeral hosting filesystems may be lost after restarts or redeployments. Configure persistent storage or migrate to a managed database before relying on stored data.
- Do not assume a local Docker volume automatically persists in a cloud deployment.

## Testing

Backend tests are located in `backend/tests/`. From the repository root, with the dependencies installed:

```bash
pytest backend/tests
```

Frontend scripts are defined in `frontend/package.json`:

```bash
cd frontend
npm run lint
npm run build
```

Run the checks in your environment and investigate failures before deployment.

## Security and Privacy Notes

- This project is not a substitute for clinical assessment, emergency services, or professional medical advice.
- Use synthetic data during development and testing.
- Do not commit API keys, administrator passwords, signing secrets, real patient records, or private uploads.
- Use a strong unique `ADMIN_SECRET_KEY` and unique admin credentials.
- Restrict CORS to trusted frontend origins in deployed environments.
- Protect administrative endpoints and review access controls before deployment.
- Assess applicable privacy, security, and regulatory obligations independently; this README does not claim regulatory compliance.

## License and Attribution

See [`LICENSE.txt`](LICENSE.txt) for the existing license and copyright attribution. Preserve required legal notices when redistributing or modifying the project.
