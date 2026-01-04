# FastAPI Authentication Microservice

A high-performance, asynchronous authentication microservice built with FastAPI, PostgreSQL, and Redis. This service provides a robust OTP (One-Time Password) based authentication flow with signed identity proofs.

## 🚀 Features

- **OTP Authentication**: Generate and verify email-based One-Time Passwords.
- **Asynchronous Database**: Built with `SQLAlchemy` and `asyncpg` for non-blocking database operations.
- **Redis Integration**: High-speed storage for OTPs and rate-limiting data.
- **Signed Identity Proofs**: Uses HMAC SHA256 to provide verifiable identity tokens upon successful verification.
- **Rate Limiting**: Integrated rate limiting using Redis to prevent brute-force attacks and abuse.
- **Containerized**: Ready for deployment with Docker and Docker Compose.
- **Email Delivery**: SMTP integration for sending verification codes.

## 🛠 Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: [PostgreSQL](https://www.postgresql.org/)
- **Cache/Task Store**: [Redis](https://redis.io/)
- **ORM**: [SQLAlchemy (Async)](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- **Validation**: [Pydantic v2](https://docs.pydantic.dev/latest/)
- **Containerization**: [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)

## 📂 Project Structure

```text
app/
├── api/             # API Routes and Routers
├── core/            # Configuration and Database setup
├── models/          # SQLAlchemy Models
├── schemas/         # Pydantic Schemas
├── services/        # Business logic (OTP, Email, Rate Limit, etc.)
└── main.py          # FastAPI application entry point
```

## ⚙️ Setup & Installation

### Prerequisites

- Docker and Docker Compose
- Python 3.10+ (if running locally)

### Environment Variables

Create a `.env` file in the root directory and configure the following:

```env
PROJECT_NAME="Authentication Microservice"
SECRET_KEY="your-super-secret-key"

# Database
POSTGRES_SERVER=auth-service-db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=auth_db
POSTGRES_PORT=5432

# Redis
REDIS_HOST=auth-service-redis
REDIS_PORT=6379

# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
EMAILS_FROM_EMAIL=noreply@example.com
EMAILS_FROM_NAME="Auth Service"
```

### Running with Docker

1. Clone the repository.
2. Build and start the containers:
   ```bash
   docker-compose up --build
   ```
3. The API will be available at `http://localhost:8013`.
4. Access the interactive API documentation at `http://localhost:8013/docs`.

## 📡 API Endpoints

### Auth

- **POST `/api/v1/auth/send-code`**: Request a verification code to be sent to an email.
- **POST `/api/v1/auth/verify-code`**: Verify the received code and get a signed identity proof.

### General

- **GET `/`**: Root health check/welcome message.

## 🔒 Security

This service uses HMAC SHA256 signatures for identity proofs. When a user is successfully verified, the service returns a payload containing user details and a signature. Other microservices can verify this signature using the same `SECRET_KEY` to trust the identity without re-verifying the email.
