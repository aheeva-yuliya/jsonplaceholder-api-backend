# JSONPlaceholder API Backend

A full-featured RESTful backend API that replicates the structure of JSONPlaceholder, with enhancements including full CRUD support, JWT-based authentication, structured relational data storage, and containerized deployment.

## Features

- Full CRUD operations for users
- JWT-based authentication
- Relational data storage with PostgreSQL
- Docker containerization
- Automatic database seeding with JSONPlaceholder data
- Input validation and error handling
- API documentation with Swagger UI

## Tech Stack

- Python 3.11
- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT + bcrypt for authentication
- Docker + Docker Compose

## Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)

## Getting Started

1. Clone the repository:
```bash
git clone <repository-url>
cd jsonplaceholder-api-backend
```

2. Start the application using Docker Compose:
```bash
docker compose up --build
```

The API will be available at `http://localhost:8000`

> Note: You may see a warning about the obsolete `version` attribute in docker-compose.yml. This warning can be safely ignored as it doesn't affect functionality.

> Note: The database is automatically initialized with sample data from JSONPlaceholder when the application starts for the first time.

## API Documentation

Once the application is running, you can access:
- Swagger UI documentation: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`

## API Usage Examples

### Authentication

#### Register a New User
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "phone": "123-456-7890",
    "website": "test.com",
    "address": {
      "street": "Test Street",
      "suite": "Test Suite",
      "city": "Test City",
      "zipcode": "12345",
      "geo": {
        "lat": "0",
        "lng": "0"
      }
    },
    "company": {
      "name": "Test Company",
      "catchPhrase": "Test Phrase",
      "bs": "Test BS"
    }
  }'
```

#### Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=password123"
```

The login response will include an access token:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

### Users API

All user endpoints require authentication. Include the token in the Authorization header:
```bash
-H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

> Note: For the users endpoints, make sure to include a trailing slash (/) in the URL to avoid redirects.

#### Get All Users
```bash
curl http://localhost:8000/users/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Example response:
```json
[
  {
    "name": "Leanne Graham",
    "username": "Bret",
    "email": "Sincere@april.biz",
    "phone": "1-770-736-8031 x56442",
    "website": "hildegard.org",
    "id": 1,
    "address": {
      "street": "Kulas Light",
      "suite": "Apt. 556",
      "city": "Gwenborough",
      "zipcode": "92998-3874",
      "id": 1,
      "user_id": 1,
      "geo": {
        "lat": "-37.3159",
        "lng": "81.1496",
        "id": 1,
        "address_id": 1
      }
    },
    "company": {
      "name": "Romaguera-Crona",
      "catchPhrase": "Multi-layered client-server neural-net",
      "bs": "harness real-time e-markets",
      "id": 1,
      "user_id": 1
    }
  },
  // ... more users ...
]
```

#### Get Specific User
```bash
curl http://localhost:8000/users/1 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Example response:
```json
{
  "name": "Leanne Graham",
  "username": "Bret",
  "email": "Sincere@april.biz",
  "phone": "1-770-736-8031 x56442",
  "website": "hildegard.org",
  "id": 1,
  "address": {
    "street": "Kulas Light",
    "suite": "Apt. 556",
    "city": "Gwenborough",
    "zipcode": "92998-3874",
    "id": 1,
    "user_id": 1,
    "geo": {
      "lat": "-37.3159",
      "lng": "81.1496",
      "id": 1,
      "address_id": 1
    }
  },
  "company": {
    "name": "Romaguera-Crona",
    "catchPhrase": "Multi-layered client-server neural-net",
    "bs": "harness real-time e-markets",
    "id": 1,
    "user_id": 1
  }
}
```

#### Update User
```bash
curl -X PUT http://localhost:8000/users/1 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Name",
    "phone": "987-654-3210"
  }'
```

> Note: Users can only update their own profile. Attempting to update another user's profile will result in a "Not authorized to update this user" error.

Example response:
```json
{
  "name": "Updated Name",
  "username": "testuser123",
  "email": "test123@example.com",
  "phone": "987-654-3210",
  "website": "test.com",
  "id": 11,
  "address": {
    "street": "Test Street",
    "suite": "Test Suite",
    "city": "Test City",
    "zipcode": "12345",
    "id": 11,
    "user_id": 11,
    "geo": {
      "lat": "0",
      "lng": "0",
      "id": 11,
      "address_id": 11
    }
  },
  "company": {
    "name": "Test Company",
    "catchPhrase": "Test Phrase",
    "bs": "Test BS",
    "id": 11,
    "user_id": 11
  }
}
```

#### Delete User
```bash
curl -X DELETE http://localhost:8000/users/1 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

> Note: Users can only delete their own profile. Attempting to delete another user's profile will result in a "Not authorized to delete this user" error.

The delete operation returns a 204 No Content response on success. After deletion, attempting to access the deleted user's profile will result in a "Could not validate credentials" error.

## Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run the application:
```bash
uvicorn app.main:app --reload
```

## Testing

### Prerequisites for Testing
1. Make sure you have Python 3.11+ installed
2. Create and activate a virtual environment:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

3. Install test dependencies:
```bash
pip install -r requirements.txt
```

### Running Tests
You can run tests while the application is running in Docker - the tests use an isolated in-memory SQLite database.

Run all tests:
```bash
pytest
```

Run tests with verbose output:
```bash
pytest -v
```

Run a specific test:
```bash
pytest tests/test_api.py::test_register_user
```

The test suite includes:
- User registration
- Authentication
- Authorization checks
- CRUD operations
- Data validation

Note: The tests use an in-memory SQLite database for isolation and speed, so they won't affect your running application's PostgreSQL database.

## Environment Variables

Create a `.env` file with the following variables:
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/jsonplaceholder
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## License

MIT