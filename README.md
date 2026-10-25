 <div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:6D597A,50:B56576,100:E56B6F&height=200&section=header&text=MediPilot&fontSize=60&fontColor=FFFFFF&fontAlignY=38&desc=Healthcare,%20thoughtfully%20coordinated.&descAlignY=58&descSize=17" width="100%" />

**Healthcare appointment scheduling, powered by conversational AI.**

A full-stack healthcare scheduling application that combines React, FastAPI, and LangGraph to guide users through appointment booking, check doctor availability, prevent double bookings, and provide an administration dashboard for doctor management and system observability.

<p>
  <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/LangGraph-303030?style=for-the-badge&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" />
  <img src="https://img.shields.io/badge/Groq-111111?style=for-the-badge&logoColor=white" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
</p>

</div>

---

## Overview

MediPilot simplifies healthcare appointment scheduling through an AI-assisted conversational interface. Instead of navigating multiple forms, users can describe their appointment needs naturally, while the scheduling workflow gathers missing information, searches doctors, checks available slots, and confirms bookings.

The application also includes a protected administration area for maintaining doctor records, importing validated JSON data, and monitoring API traffic and scheduling workflow performance.

> MediPilot is a development and portfolio project, not a production clinical system. It does not replace professional medical advice or emergency services.

## Features

### Conversational Appointment Scheduling
- Natural-language conversations for collecting doctor, specialty, date, time, and patient details.
- Persistent conversation state using LangGraph and thread identifiers.
- Doctor search and appointment availability checks.
- Interactive available-time options and a visit summary panel.
- Appointment confirmation with database-level protection against double booking.
- Workflow activity tracing, request retries, and conversation reset.

### Administration Dashboard
- Protected administrator login with signed, expiring bearer tokens.
- Doctor directory with search, specialty filtering, sorting, and pagination.
- JSON doctor-data import with validation and preview before saving.
- Controlled directory reset with explicit confirmation.
- Observability dashboard for API requests, failures, latency, booking outcomes, and workflow execution metrics.

### Interface and Reliability
- Responsive layouts for desktop, tablet, and mobile.
- Keyboard navigation, visible focus indicators, and reduced-motion support.
- Backend health-status indicator.
- Modular frontend components and backend services.
- Automated backend and frontend tests.
- Docker and Docker Compose support.

## AI Agent Architecture

MediPilot uses **LangGraph** to coordinate the appointment scheduling workflow. The language model extracts intent and relevant appointment details, while deterministic routing and database-backed tools handle scheduling operations.

```text
User Message
     |
     v
Analyze Request (LLM)
     |
     v
Route Request
     |
     +----> Search Doctors
     |
     +----> Find Available Dates
     |
     +----> Check Availability
     |           |
     |           v
     |     Book Appointment
     |
     +----> General Response
                 |
                 v
            Final Response
```

- **Intent analysis:** Extracts appointment details from natural-language messages using a Groq-hosted language model.
- **Workflow routing:** Selects the appropriate scheduling action based on the request and existing conversation state.
- **Scheduling tools:** Search doctors, retrieve available dates, check time slots, and create appointments.
- **State persistence:** Uses SQLite-backed LangGraph checkpoints to continue conversations across requests.
- **Booking integrity:** Uses a unique database constraint on doctor, date, and time to prevent conflicting bookings.
- **Workflow tracing:** Reports executed workflow steps for the interface's agent activity panel.

## Technology Stack

| Layer | Technologies |
|---|---|
| Frontend | React, Vite, JavaScript, CSS |
| Backend | Python, FastAPI, Uvicorn, Pydantic |
| AI Workflow | LangGraph, LangChain |
| Language Model | Groq |
| Database | SQLite, SQLAlchemy |
| State Persistence | LangGraph SQLite checkpoint integration |
| Containerization | Docker, Docker Compose, Nginx |
| Testing | Pytest, FastAPI TestClient, Vitest |
| Code Quality | Oxlint |

## Project Structure

```text
MediPilot/
├── backend/
│   ├── app/
│   │   ├── api.py
│   │   ├── checkpointer.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── doctor_import.py
│   │   ├── graph.py
│   │   ├── models.py
│   │   ├── state.py
│   │   └── tools.py
│   ├── tests/
│   └── Dockerfile
├── data/
│   └── doctors.json
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── features/
│   │   │   ├── schedule/
│   │   │   └── admin/
│   │   ├── hooks/
│   │   ├── lib/
│   │   ├── services/
│   │   ├── styles/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── nginx.conf
│   └── Dockerfile
├── notebooks/
│   └── scheduling_demo.ipynb
├── .env.example
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.11
- Node.js 22.12 or newer
- npm
- Docker and Docker Compose (optional)

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Check backend health |
| `POST` | `/api/v1/schedule` | Submit a scheduling message |
| `GET` | `/api/v1/conversations/{thread_id}` | Retrieve conversation state |
| `POST` | `/api/v1/admin/login` | Authenticate an administrator |
| `GET` | `/api/v1/admin/doctors` | Retrieve doctor records |
| `POST` | `/api/v1/admin/doctors/preview` | Validate and preview doctor data |
| `POST` | `/api/v1/admin/doctors/initialize` | Import validated doctor records |
| `POST` | `/api/v1/admin/doctors/reset` | Reset directory data |
| `GET` | `/api/v1/admin/observability` | Retrieve API and workflow metrics |

Interactive API documentation is available at `/docs` when the backend is running.

## Testing

### Backend

Run from the repository root:

```bash
python -m pytest backend/tests
```

### Frontend

Run from the frontend directory:

```bash
npm test
npm run lint
npm run build
```

The backend tests use a temporary database and a fake language model for workflow testing. The repository does not include automated browser tests, and the tests do not validate real language-model behavior.

## Deployment

MediPilot includes Dockerfiles and a Docker Compose configuration for running the frontend and backend together.

For separate frontend and backend deployments:

- Configure `FRONTEND_URL` with the deployed frontend origin.
- Configure `VITE_API_URL` with the backend URL during the frontend build.
- Store secrets in backend environment variables.
- Configure persistent storage for the SQLite database and workflow checkpoints.
- Verify CORS, authentication, API connectivity, and database persistence in the target environment.

SQLite data stored on an ephemeral hosting filesystem may be lost after a restart or redeployment. Use persistent storage or a managed database before relying on stored appointment data.

## Security and Privacy

- Use synthetic patient information during development and testing.
- Never commit API keys, passwords, signing secrets, or real patient records.
- Keep administrative endpoints protected and use strong, unique credentials.
- Restrict CORS to trusted frontend origins.
- Review database persistence, access controls, and deployment configuration before use.

MediPilot does not currently provide rate limiting, an audit log, encryption at rest, or a data-retention policy. The project has not been represented as compliant with healthcare privacy regulations. Conduct an independent security, privacy, and regulatory review before any real-world deployment.

---

<div align="center">

**MediPilot — Healthcare, thoughtfully coordinated.**

<sub>Built with React, FastAPI, LangGraph, and conversational AI.</sub>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:6D597A,50:B56576,100:E56B6F&height=100&section=footer" width="100%" />

</div>
