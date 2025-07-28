# Inventory Management API

A simple, secure Flask-based REST API for managing inventory.

## Tech Stack

- **Backend**: Flask (Python web framework)
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: JWT (JSON Web Tokens)
- **Password Hashing**: Werkzeug security utilities
- **CORS**: Flask-CORS for cross-origin requests

## Project Structure

```
inventory_app/
│
├── app.py          # Main Flask application
├── models.py       # Database models (User, Product)
├── test_api.py     # Automated test script
├── database.db     # SQLite database (auto-generated)
└── README.md       # This file
```

## Installation & Setup

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

### Step 1: Clone the Repository

```bash
git clone <your-repo-url>
cd inventory_app
```

### Step 2: Install Dependencies

```bash
pip install flask flask_sqlalchemy flask_cors pyjwt werkzeug requests
```

### Step 3: Run the Application

```bash
python app.py
```

The API will start running on `http://localhost:8080`

You should see output similar to:
```
* Running on http://127.0.0.1:8080
* Debug mode: on
```

### Add a Product (using the token)

```bash
curl -X POST http://localhost:8080/products \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "name": "Laptop",
    "type": "Electronics",
    "sku": "LAP-001",
    "description": "Gaming laptop",
    "quantity": 10,
    "price": 1299.99
  }'
```

## Testing

### Automated Testing

Run the provided test script to verify all endpoints:

```bash
python test_api.py
```

The test script will:
1. Register a test user
2. Login and obtain a JWT token
3. Add a product
4. Update product quantity
5. Retrieve and verify product data

Expected output:
```
User Registration: PASSED
Login Test: PASSED
Add Product: PASSED
Update Quantity: PASSED, Updated quantity: 15
Get Products: PASSED (Quantity = 15)
```

## API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/register` | Register new user | No |
| POST | `/login` | User login | No |
| POST | `/products` | Add new product | Yes |
| GET | `/products` | Get all products | Yes |
| PUT | `/products/{id}/quantity` | Update product quantity | Yes |

For detailed API documentation, see [API_DOCS.md](API_DOCS.md) or visit the Swagger documentation when the server is running.

## Database Schema

### Users Table
- `id` (Integer, Primary Key)
- `username` (String, Unique)
- `password_hash` (String)

### Products Table
- `id` (Integer, Primary Key)
- `name` (String, Required)
- `type` (String, Optional)
- `sku` (String, Unique, Required)
- `image_url` (String, Optional)
- `description` (String, Optional)
- `quantity` (Integer, Default: 0)
- `price` (Float, Required)

## Security Features

- **Password Hashing**: All passwords are hashed using Werkzeug's secure hash functions
- **JWT Authentication**: Stateless authentication with expiring tokens (1 hour)
- **Protected Endpoints**: All product operations require valid JWT tokens

## Configuration

### Environment Variables

You can customize the application by modifying these settings in `app.py`:

- `SECRET_KEY`: JWT signing key (change for production!)
- `SQLALCHEMY_DATABASE_URI`: Database connection string
- `Token Expiration`: Currently set to 1 hour

### Production Deployment

For production deployment:

1. **Change the SECRET_KEY** to a secure, random value
2. **Use a production database** (PostgreSQL, MySQL) instead of SQLite
3. **Disable debug mode** by setting `debug=False`
