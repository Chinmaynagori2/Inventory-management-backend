
# Inventory Management API – Documentation

Base URL: `http://localhost:8080`

---

## Authentication

All product-related routes require a JWT token passed in the header:

```
Authorization: Bearer <access_token>
```

---

##  User Routes

### **POST `/register`**

Registers a new user.

#### Request Body
```json
{
  "username": "string",
  "password": "string"
}
```

#### Response
- `201 Created` – User registered successfully
- `409 Conflict` – Username already exists

---

### **POST `/login`**

Logs in a registered user and returns a JWT token.

#### Request Body
```json
{
  "username": "string",
  "password": "string"
}
```

#### Response
```json
{
  "access_token": "string"
}
```

- `200 OK` – Login successful
- `401 Unauthorized` – Invalid credentials

---

## Product Routes (Require Auth)

### **POST `/products`**

Adds a new product.

#### Headers
```
Authorization: Bearer <access_token>
```

#### Request Body
```json
{
  "name": "Phone",
  "type": "Electronics",
  "sku": "PHN-001",
  "image_url": "https://example.com/image.jpg",
  "description": "Latest model",
  "quantity": 5,
  "price": 999.99
}
```

#### Response
```json
{
  "product_id": 1
}
```

- `201 Created`

---

### **PUT `/products/<product_id>/quantity`**

Updates the quantity of a specific product.

#### Headers
```
Authorization: Bearer <access_token>
```

#### Request Body
```json
{
  "quantity": 15
}
```

#### Response
```json
{
  "product_id": 1,
  "quantity": 15
}
```

- `200 OK` – Quantity updated
- `404 Not Found` – Product not found

---

### **GET `/products`**

Fetches the list of all products.

#### Headers
```
Authorization: Bearer <access_token>
```

#### Response
```json
[
  {
    "id": 1,
    "name": "Phone",
    "type": "Electronics",
    "sku": "PHN-001",
    "image_url": "https://example.com/image.jpg",
    "description": "Latest model",
    "quantity": 15,
    "price": 999.99
  }
]
```

- `200 OK` – Returns product list
