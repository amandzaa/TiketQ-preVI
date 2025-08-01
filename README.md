# TiketQ - Ticket Management REST API

A modern REST API for managing event tickets built with Flask, SQLAlchemy, and PostgreSQL. Features a modular architecture with comprehensive CRUD operations, data validation, and Docker containerization.

## 🚀 Features

- ✅ Complete CRUD operations for tickets
- ✅ Input validation with detailed error messages
- ✅ Comprehensive error handling (400, 404, 500)
- ✅ PostgreSQL database with SQLAlchemy ORM
- ✅ Docker containerization with docker-compose
- ✅ ISO datetime validation
- ✅ Health check endpoint
- ✅ Production-ready with Gunicorn
- ✅ Modular architecture with blueprints
- ✅ Marshmallow schemas for data validation

## 🏗️ Project Structure

```
TiketQ-preVI/
├── app/                    # Main application package
│   ├── __init__.py         # App factory and extensions
│   ├── config/             # Configuration settings
│   │   ├── __init__.py
│   │   └── config.py
│   ├── models/             # Database models
│   │   ├── __init__.py
│   │   └── tiketq.py
│   ├── routes/             # Route blueprints
│   │   ├── __init__.py
│   │   ├── ticketing.py
│   │   └── health.py
│   ├── schemas/            # Marshmallow schemas
│   │   ├── __init__.py
│   │   └── ticket_schema.py
│   └── extensions.py       # Flask extensions
├── migrations/             # Database migrations
├── tests/                  # Unit tests
├── docker-compose.yml      # Docker services
├── Dockerfile             # Container configuration
├── requirements.txt        # Python dependencies
└── run.py                 # Application entry point
```

## 🚀 Quick Start

### Using Docker (Recommended)

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd TiketQ-preVI
   ```

2. **Start the application**

   ```bash
   docker-compose up --build
   ```

3. **Access the API**
   - API: http://localhost:5000
   - Health Check: http://localhost:5000/api/health

### Local Development

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables**

   ```bash
   export FLASK_ENV=development
   export DATABASE_URL=sqlite:///tiketq.db
   ```

3. **Run the application**
   ```bash
   python run.py
   ```

## 📋 API Endpoints

### Base URL: `http://localhost:5000`

### Health Check

```http
GET /api/health
```

**Response:**

```json
{
  "status": "healthy",
  "service": "TiketQ API"
}
```

### Ticket Management

#### 1. List All Tickets

```http
GET /tickets
```

**Optional Query Parameters:**

- `isUsed`: Filter by usage status (true/false)

**Response:**

```json
[
  {
    "id": 1,
    "eventName": "Concert 2025",
    "location": "Madison Square Garden",
    "time": "2025-03-15T19:30:00",
    "isUsed": false
  }
]
```

#### 2. Get Specific Ticket

```http
GET /tickets/:id
```

#### 3. Create New Ticket

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

#### 4. Update Ticket Usage

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

#### 5. Delete Ticket

```http
DELETE /tickets/:id
```

## 🔍 Data Validation

### Ticket Schema Rules:

- `eventName`: Required, 1-200 characters
- `location`: Required, 1-200 characters
- `time`: Required, valid ISO datetime format, must be in the future
- `isUsed`: Optional boolean, defaults to false

### Example Validation Error:

```json
{
  "error": "Bad Request",
  "messages": {
    "eventName": ["Length must be between 1 and 200."],
    "time": ["Time must be in the future."]
  }
}
```

## 🧪 Testing Examples

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

## 🗄️ Database Schema

```sql
CREATE TABLE ticket (
    id INTEGER PRIMARY KEY,
    eventName VARCHAR(200) NOT NULL,
    location VARCHAR(200) NOT NULL,
    time DATETIME NOT NULL,
    isUsed BOOLEAN DEFAULT FALSE NOT NULL
);
```

## ⚙️ Environment Variables

| Variable       | Description                | Default               |
| -------------- | -------------------------- | --------------------- |
| `FLASK_ENV`    | Flask environment          | `development`         |
| `DATABASE_URL` | Database connection string | `sqlite:///tiketq.db` |
| `SECRET_KEY`   | Flask secret key           | `dev`                 |

## 🐳 Docker Configuration

The application includes:

- **PostgreSQL 15** database service
- **Python 3.12** application container
- **Gunicorn** WSGI server for production
- **Volume persistence** for database data

## 🛠️ Technologies Used

- **Flask 2.3.3** - Web framework
- **SQLAlchemy 3.0.5** - ORM for database operations
- **PostgreSQL 15** - Primary database
- **Marshmallow 3.20.1** - Data validation and serialization
- **Docker & Docker Compose** - Containerization
- **Gunicorn 21.2.0** - WSGI HTTP Server
- **Flask-Migrate 4.0.5** - Database migrations
- **Flask-CORS 4.0.0** - Cross-origin resource sharing

## 🔧 Development

### Running Tests

```bash
python -m pytest tests/
```

### Database Migrations

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### Code Formatting

```bash
pip install black
black app/
```

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

For support, email amandzaa@gmail.com or create an issue in this repository.
