# Ticket Management REST API

A simple REST API for managing event tickets built with Flask, SQLAlchemy, and PostgreSQL.

## Features

- ✅ Complete CRUD operations for tickets
- ✅ Input validation with detailed error messages
- ✅ Comprehensive error handling (400, 404, 500)
- ✅ PostgreSQL database with SQLAlchemy ORM
- ✅ Docker containerization
- ✅ ISO datetime validation
- ✅ Health check endpoint
- ✅ Production-ready with Gunicorn

## Quick Start

### Using Docker (Recommended)

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd ticket-api
   ```

2. **Start the application**

   ```bash
   docker-compose up --build
   ```

3. **The API will be available at:**
   - API: http://localhost:5000
   - pgAdmin: http://localhost:5050 (admin@ticket.com / admin)

### Local Development

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables**

   ```bash
   export FLASK_ENV=development
   export DATABASE_URL=sqlite:///tickets.db  # Or PostgreSQL URL
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

## API Endpoints

### Base URL: `http://localhost:5000`

### 1. Health Check

```http
GET /health
```

**Response:**

```json
{
  "status": "healthy",
  "timestamp": "2025-01-29T10:30:00.000Z"
}
```

### 2. List All Tickets

```http
GET /tickets
```

**Optional Query Parameters:**

- `isUsed`: Filter by usage status (true/false)

**Response:**

```json
{
  "tickets": [
    {
      "id": 1,
      "eventName": "Concert 2025",
      "location": "Madison Square Garden",
      "time": "2025-03-15T19:30:00",
      "isUsed": false,
      "created_at": "2025-01-29T10:30:00.000Z",
      "updated_at": "2025-01-29T10:30:00.000Z"
    }
  ],
  "count": 1
}
```

### 3. Get Specific Ticket

```http
GET /tickets/:id
```

**Response:**

```json
{
  "ticket": {
    "id": 1,
    "eventName": "Concert 2025",
    "location": "Madison Square Garden",
    "time": "2025-03-15T19:30:00",
    "isUsed": false,
    "created_at": "2025-01-29T10:30:00.000Z",
    "updated_at": "2025-01-29T10:30:00.000Z"
  }
}
```

### 4. Create New Ticket

```http
POST /tickets
Content-Type: application/json
```

**Request Body:**

```json
{
  "eventName": "Concert 2025",
  "location": "Madison Square Garden",
  "time": "2025-03-15T19:30:00",
  "isUsed": false
}
```

**Response (201):**

```json
{
  "message": "Ticket created successfully",
  "ticket": {
    "id": 1,
    "eventName": "Concert 2025",
    "location": "Madison Square Garden",
    "time": "2025-03-15T19:30:00",
    "isUsed": false,
    "created_at": "2025-01-29T10:30:00.000Z",
    "updated_at": "2025-01-29T10:30:00.000Z"
  }
}
```

### 5. Mark Ticket as Used

```http
PATCH /tickets/:id
Content-Type: application/json
```

**Request Body:**

```json
{
  "isUsed": true
}
```

**Response:**

```json
{
  "message": "Ticket updated successfully",
  "ticket": {
    "id": 1,
    "eventName": "Concert 2025",
    "location": "Madison Square Garden",
    "time": "2025-03-15T19:30:00",
    "isUsed": true,
    "created_at": "2025-01-29T10:30:00.000Z",
    "updated_at": "2025-01-29T10:32:00.000Z"
  }
}
```

### 6. Delete Ticket

```http
DELETE /tickets/:id
```

**Response:**

```json
{
  "message": "Ticket 1 deleted successfully"
}
```

## Data Validation

### Ticket Creation Rules:

- `eventName`: Required, 1-200 characters
- `location`: Required, 1-200 characters
- `time`: Required, valid ISO datetime format, must be in the future
- `isUsed`: Optional boolean, defaults to false

### Example Validation Errors:

```json
{
  "error": "Validation Error",
  "message": "Input validation failed",
  "details": {
    "eventName": ["Event name is required"],
    "time": ["Event time must be in the future"]
  }
}
```

## Error Handling

The API returns consistent error responses:

### 400 Bad Request

```json
{
  "error": "Bad Request",
  "message": "The request could not be understood by the server"
}
```

### 404 Not Found

```json
{
  "error": "Not Found",
  "message": "Ticket with id 999 not found"
}
```

### 500 Internal Server Error

```json
{
  "error": "Internal Server Error",
  "message": "An unexpected error occurred"
}
```

## Testing Examples

### Using curl:

**Create a ticket:**

```bash
curl -X POST http://localhost:5000/tickets \
  -H "Content-Type: application/json" \
  -d '{
    "eventName": "Rock Concert",
    "location": "Stadium Arena",
    "time": "2025-06-15T20:00:00"
  }'
```

**Get all tickets:**

```bash
curl http://localhost:5000/tickets
```

**Mark ticket as used:**

```bash
curl -X PATCH http://localhost:5000/tickets/1 \
  -H "Content-Type: application/json" \
  -d '{"isUsed": true}'
```

## Database Schema

```sql
CREATE TABLE tickets (
    id SERIAL PRIMARY KEY,
    eventName VARCHAR(200) NOT NULL,
    location VARCHAR(200) NOT NULL,
    time TIMESTAMP NOT NULL,
    isUsed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Environment Variables

- `FLASK_ENV`: Set to 'development' or 'production'
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: Flask secret key for security
- `PORT`: Port to run the application (default: 5000)

## Production Deployment

The application is production-ready with:

- Gunicorn WSGI server
- PostgreSQL database
- Docker containerization
- Health checks
- Error logging
- Security best practices

## Technologies Used

- **Flask**: Web framework
- **SQLAlchemy**: ORM for database operations
- **PostgreSQL**: Primary database
- **Marshmallow**: Data validation and serialization
- **Docker**: Containerization
- **Gunicorn**: WSGI HTTP Server

## Project Structure

```
TiketQ-preVI/
│
├── app/                    # Main application package
│   ├── __init__.py         # App factory, extensions, etc.
│   ├── models.py           # SQLAlchemy models (or a models/ folder for many models)
│   ├── routes.py           # Flask routes (or a routes/ folder for blueprints)
│   ├── schemas.py          # Marshmallow schemas (optional)
│   ├── extensions.py       # For db, migrate, etc. initialization
│   ├── config.py           # Configuration classes
│   ├── templates/          # Jinja2 HTML templates
│   └── static/             # Static files (CSS, JS, images)
│
├── migrations/             # Alembic migration scripts (created by flask db init)
│
├── tests/                  # Unit and integration tests
│   └── __init__.py
│
├── .env                    # Environment variables (not committed)
├── .gitignore
├── requirements.txt
├── README.md
└── run.py                  # Entry point to run the app (or wsgi.py)
```
