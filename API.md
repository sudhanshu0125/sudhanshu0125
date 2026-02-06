# API Reference

Base URL: `http://localhost:8000/api`

## Authentication

### `POST /auth/register`
Create user and return JWT.

### `POST /auth/login`
Authenticate and return JWT.

Use header:
`Authorization: Bearer <token>`

## Leads

### `GET /leads?status=Hot&q=agency`
List leads with optional filters.

### `POST /leads`
Create a lead manually.

### `PATCH /leads/{lead_id}`
Update status, approval, notes, outreach_state.

## Agent

### `POST /agent/run`
Run discovery + extraction + qualification pipeline.

Request body:
```json
{ "query": "influencer marketing agencies india", "max_results": 20 }
```

## Outreach

### `POST /outreach/trigger`
Queue outreach on email/WhatsApp/manual channel.
