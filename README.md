# 211 Civic Service Platform

## Overview
211 is an event-driven civic service platform modeled after municipal 
311 systems. It allows residents to submit service requests — such as 
reporting infrastructure issues or city maintenance needs.

When a request is submitted the platform automatically validates the 
address via real-time geocoding, generates a unique correlation ID for 
tracking, persists the record to the database, and sends an async 
notification confirming receipt.

Built as a microservices architecture to demonstrate production-quality 
API design, event-driven communication, and data privacy principles.


## Architecture
Citizen
  ↓ HTTP POST /api/v1/requests
Gateway (port 8000)
  ├── REST → location-service (Nominatim geocoding)
  ├── REST → request-service (save to Postgres)
  └── RabbitMQ → notification-service (async SMS)

request-service → Postgres
ticket-service  → Postgres
RabbitMQ broker → notification-service consumer


## Services
Gateway
Single public entry point responsible for authentication, routing, and orchestration.

Location Service
Validates and enriches addresses using OpenStreetMap Nominatim.

Request Service
Persists citizen requests to PostgreSQL and maintains a full audit trail.

Ticket Service
Manages the lifecycle of each request, including all status transitions.

Notification Service
Consumes RabbitMQ events and sends notifications to citizens.

Communication Patterns
REST (httpx)
Used when a response is required before continuing — e.g., address validation, request creation.

RabbitMQ (aio‑pika)
Used for fire‑and‑forget operations — e.g., notifications that should not block the main request flow.

## Tech Stack
1. Framework | FastAPI running on Python 3.12.
2. Database | PostgreSQL 16 for persistent storage.
3. Message Broker | RabbitMQ 3 for asynchronous communication.
4. ORM | SQLAlchemy 2.0 for database interaction.
5. Async HTTP | httpx for non‑blocking HTTP requests.
6. Message Queue Client | aio‑pika for interacting with RabbitMQ.
7. Geocoding | OpenStreetMap Nominatim for address validation and enrichment.
8. Containerization | Docker and Docker Compose for local development and deployment.
9. Data Validation | Pydantic v2 for request/response schema validation.

## Getting Started
### Prerequisites
- Docker Desktop
- Git

### Installation

1. Clone the repository
\```bash
git clone https://github.com/yourusername/211.git
cd 211
\```

2. Configure environment
\```bash
cp .env.example .env
# Edit .env with your values
\```

3. Start all services
\```bash
docker compose up --build
\```

4. Verify all services are running
\```bash
docker ps
\```

### Test the API

Submit a service request:
\```bash
curl -X POST http://localhost:8000/api/v1/requests/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer test-token" \
  -d '{
    "full_name": "Maria Garcia",
    "address": "450 North 1st Street, San Jose, CA",
    "issue": "Broken streetlight",
    "contact": "408-555-0192"
  }'
\```

Expected response:
\```json
{
  "correlation_id": "uuid",
  "status": "pending",
  "message": "Your request has been received and is being processed"
}
\```
## API Reference

### Submit a Service Request
`POST /api/v1/requests/`

**Request body:**
| Field | Type | Description |
|---|---|---|
| full_name | string | Citizen's full name |
| address | string | Address of the issue |
| issue | string | Description of the problem |
| contact | string | Phone or email for notifications |

**Response:** `202 Accepted`


## Security
- All internal services are unexposed — only the gateway is publicly accessible
- PII (names, addresses, contact info) is never written to logs
- Secrets managed via environment variables — never hardcoded
- JWT authentication on all public endpoints (stub in development)
- Data minimization — each service only receives the data it needs
- CCPA-conscious design — citizen data protected at every layer

> Note: JWT authentication is currently a stub returning a mock user.
> Full implementation with token issuance, refresh tokens, and
> revocation is planned for production.

## Development Notes


## Roadmap

- [ ] Full JWT authentication with refresh token rotation
- [ ] Role-based access control (citizen vs admin vs field worker)
- [ ] Department routing based on issue type and district
- [ ] Real SMS/email notifications via Twilio/SendGrid
- [ ] Citizen-facing status tracking endpoint
- [ ] Admin dashboard for city workers
- [ ] Cloud deployment (AWS/GCP)
- [ ] CI/CD pipeline
