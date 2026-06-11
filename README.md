# Document Insights API

Async document processing service built using:

- FastAPI
- MongoDB
- Redis
- Docker Compose

---

## Features

### Submit Document

POST /documents

Stores document and queues processing.

---

### Get Document Status

GET /documents/{document_id}

Returns:

- queued
- processing
- completed
- failed

---

### User Documents

GET /users/{user_id}/documents

Supports:

- pagination
- status filter

---

### Health Check

GET /health

Checks:

- MongoDB
- Redis

---

## Rate Limiting

Maximum 3 active jobs per user.

Returns:

HTTP 429

when exceeded.

---

## Content Cache

Identical content submitted by same user returns cached summary immediately.

Redis TTL used.

---

## Run

docker compose up --build

Swagger:

http://localhost:5000/docs

---

## Tests

pytest -v
