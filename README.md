# Raftaar - Bike Sharing Platform MVP

A FastAPI-based bike-sharing platform inspired by Rapido, allowing users to book bikes for short-distance urban travel.

## Tech Stack

- **Backend:** Python 3.11+ with FastAPI
- **Database:** PostgreSQL with PostGIS for geospatial queries
- **Frontend:** React (to be built)
- **Payment:** Razorpay (mocked in MVP)
- **Deployment:** Docker & Docker Compose

## Quick Start

### Prerequisites

- Docker & Docker Compose installed
- Git

### Setup (Local with Docker)

```bash
# Clone the repository
git clone https://github.com/adityanandanx/raftaar.git
cd raftaar

# Copy environment file
cp .env.example .env

# Build and start containers
docker-compose up --build

# Run migrations (in separate terminal)
docker-compose exec backend alembic upgrade head

# Access the API
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
# Health Check: http://localhost:8000/health
```

### Setup (Local without Docker)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Start PostgreSQL (ensure PostGIS extension is installed)
# Then run migrations
alembic upgrade head

# Start the server
uvicorn app.main:app --reload
```

## Project Structure

```
raftaar/
├── app/
│   ├── models/          # SQLAlchemy ORM models
│   ├── schemas/         # Pydantic request/response schemas
│   ├── routes/          # API endpoints
│   ├── services/        # Business logic
│   └── main.py          # FastAPI app initialization
├── config/
│   ├── settings.py      # Environment configuration
│   └── database.py      # Database connection
├── migrations/          # Alembic database migrations
├── tests/               # Pytest test suite
├── requirements.txt     # Python dependencies
├── docker-compose.yml   # Docker Compose configuration
├── Dockerfile          # Docker image definition
└── .env.example        # Environment variables template
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py -v
```

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Add user table"

# Apply migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1
```

### API Documentation

Once the server is running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Features (MVP)

### Customer Features
- User registration and authentication
- View nearby bikes on a map
- Reserve a bike for 5 minutes
- Start trip by scanning QR code
- Auto-calculated trip pricing (₹2 base + ₹0.20/min)
- End trip at any station
- Automatic payment processing
- Trip receipts via email
- Support tickets and auto-refunds within 24 hours
- Trip history and statistics

### Admin Features
- Manage stations and bikes
- Monitor all trips in real-time
- View revenue and utilization metrics
- Update pricing rules
- Create discount codes
- Manage support tickets and refunds

## API Endpoints (To Be Built)

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/me` - Get user profile
- `PUT /auth/profile` - Update profile

### Map & Discovery
- `GET /map/nearby-bikes?lat=X&lng=Y&radius=5` - Find bikes near location
- `GET /map/all-stations` - Get all stations

### Booking & Trips
- `POST /bookings/reserve` - Reserve a bike
- `POST /trips/start` - Start trip with QR code
- `POST /trips/end` - End trip
- `GET /trips/history` - Get trip history

### Payments
- `POST /payment-methods/add` - Save payment method
- `GET /payment-methods` - List payment methods

### Support
- `POST /support-tickets/create` - Report issue
- `GET /support-tickets` - View support tickets

### Admin
- `GET /admin/analytics/revenue` - Revenue analytics
- `GET /admin/analytics/trips` - Trip analytics
- `GET /admin/bikes` - List all bikes
- `GET /admin/stations` - List all stations

## Environment Variables

See `.env.example` for all available configuration options. Key variables:

- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - JWT secret key
- `ENVIRONMENT` - development/production
- `DEBUG` - Enable debug mode
- `RAZORPAY_API_KEY` - Razorpay API key (mocked for MVP)
- `RAZORPAY_API_SECRET` - Razorpay API secret (mocked for MVP)

## Deployment

### Docker Compose

```bash
docker-compose up -d
```

### Cloud Deployment (Fly.io or Railway)

See deployment documentation for setup instructions.

## Testing

The project uses pytest with the following test organization:

- **Unit tests:** Test individual functions and services
- **Integration tests:** Test modules together with mocked database
- **API tests:** Test HTTP endpoints end-to-end

Test coverage goals:
- Pricing Module: 100%
- Booking Module: 95%
- Geolocation Module: 90%
- Payment Module: 95%
- Other Modules: 70%

## Contributing

1. Create a feature branch (`git checkout -b feature/amazing-feature`)
2. Commit changes (`git commit -m 'Add amazing feature'`)
3. Push to branch (`git push origin feature/amazing-feature`)
4. Open a Pull Request

## License

This project is licensed under the MIT License.

## Contact

For questions or issues, please reach out or create an issue on GitHub.
