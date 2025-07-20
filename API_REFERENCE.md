# API Reference - MCP Banking Backend

## Authentication Required

All endpoints except `/health`, `/register`, and `/token` require a valid JWT token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

## Endpoints

### Authentication

#### POST /register
Register a new user account.

**Request Body:**
```json
{
  "username": "string",
  "email": "string", 
  "password": "string",
  "full_name": "string" (optional)
}
```

**Response:**
```json
{
  "id": 1,
  "username": "string",
  "email": "string",
  "full_name": "string",
  "is_active": true,
  "created_at": "2025-07-20T10:30:00"
}
```

#### POST /token
Login and get access token.

**Request Body (form-data):**
```
username=your_username
password=your_password
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

### User Information

#### GET /me
Get current user information.

**Response:**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "created_at": "2025-07-20T10:30:00"
}
```

### Account Management

#### GET /accounts
Get all accounts for the current user.

**Response:**
```json
{
  "accounts": [
    {
      "id": "ACC001",
      "account_name": "Checking Account",
      "account_type": "checking",
      "balance": 5000.0,
      "currency": "USD",
      "is_active": true,
      "created_at": "2025-07-20T10:30:00",
      "user_id": 1
    }
  ]
}
```

#### GET /accounts/{account_id}
Get details for a specific account.

**Response:**
```json
{
  "id": "ACC001",
  "account_name": "Checking Account", 
  "account_type": "checking",
  "balance": 5000.0,
  "currency": "USD",
  "is_active": true,
  "created_at": "2025-07-20T10:30:00",
  "user_id": 1
}
```

#### GET /accounts/{account_id}/balance
Get account balance.

**Response:**
```json
{
  "account_id": "ACC001",
  "balance": 5000.0,
  "currency": "USD",
  "account_name": "Checking Account"
}
```

#### GET /accounts/{account_id}/transactions
Get transaction history for an account.

**Query Parameters:**
- `limit` (optional): Number of transactions to return (default: 10)

**Response:**
```json
[
  {
    "id": "TXN001",
    "from_account_id": "ACC001",
    "to_account_id": null,
    "amount": -50.0,
    "currency": "USD",
    "description": "ATM Withdrawal",
    "transaction_type": "withdrawal",
    "status": "completed",
    "created_at": "2025-07-20T10:30:00"
  }
]
```

### Banking Operations

#### POST /transfer?from_account_id={account_id}
Transfer money between accounts.

**Query Parameters:**
- `from_account_id`: Source account ID

**Request Body:**
```json
{
  "to_account_id": "ACC002",
  "amount": 100.0,
  "currency": "USD",
  "description": "Transfer to savings" (optional)
}
```

**Response:**
```json
{
  "id": "TXN123",
  "from_account_id": "ACC001",
  "to_account_id": "ACC002", 
  "amount": 100.0,
  "currency": "USD",
  "description": "Transfer to savings",
  "transaction_type": "transfer",
  "status": "completed",
  "created_at": "2025-07-20T10:30:00"
}
```

### System

#### GET /health
Health check endpoint (no authentication required).

**Response:**
```json
{
  "status": "healthy",
  "service": "mcp-banking-backend",
  "timestamp": "2025-07-20T10:30:00",
  "database": "connected"
}
```

#### POST /config
Update MCP server configuration.

**Request Body:**
```json
{
  "mcp_server_url": "http://localhost:8080"
}
```

**Response:**
```json
{
  "message": "Configuration updated",
  "mcp_server_url": "http://localhost:8080"
}
```

### Admin

#### GET /admin/users
Get all users (admin endpoint).

**Response:**
```json
[
  {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "is_active": true,
    "created_at": "2025-07-20T10:30:00"
  }
]
```

## Error Responses

All endpoints return consistent error responses:

```json
{
  "detail": "Error message description"
}
```

Common HTTP status codes:
- `400` - Bad Request (invalid input)
- `401` - Unauthorized (missing or invalid token)
- `404` - Not Found (resource doesn't exist)
- `500` - Internal Server Error

## MCP Integration

The backend automatically calls MCP agents for:
- Account access logging
- Balance checks
- Transaction history requests
- Transfer fraud detection
- User authentication events

MCP calls are made asynchronously and don't block the API response.
