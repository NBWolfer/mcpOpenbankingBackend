# API Reference - MCP Banking Backend

## Authentication Methods

This API supports **dual authentication** for maximum flexibility:

### 1. Bearer Token (API Clients)
```
Authorization: Bearer <your_jwt_token>
```

### 2. HTTP-Only Cookies (Web Browsers)
- Automatically set on login via `/login` or `/token` endpoints
- More secure for web applications (prevents XSS attacks)
- Automatically sent by browsers on subsequent requests

**Note:** All endpoints except `/health`, `/register`, `/token`, and `/login` require authentication.

## Endpoints

### Authentication

#### POST /register
Register a new user account and automatically sync with dummy bank.

**Request Body:**
```json
{
  "username": "string",
  "email": "string", 
  "password": "string",
  "full_name": "string"
}
```

**Response:**
```json
{
  "id": 1,
  "username": "string",
  "email": "string",
  "full_name": "string",
  "customer_oid": "550e8400-e29b-41d4-a716-446655440001",
  "is_active": true,
  "created_at": "2025-07-20T10:30:00"
}
```

#### POST /token
Login with form data and get access token + HTTP-only cookie.

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
**Note:** Also sets HTTP-only cookie named `access_token`

#### POST /login
Login with JSON credentials and get access token + HTTP-only cookie.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```
**Note:** Also sets HTTP-only cookie named `access_token`

#### POST /logout
Logout and clear HTTP-only cookie.

**Response:**
```json
{
  "message": "Successfully logged out"
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
  "customer_oid": "550e8400-e29b-41d4-a716-446655440001",
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

### Dummy Bank Integration

#### GET /bank/portfolio
Get user's portfolio from dummy bank.

**Response:**
```json
{
  "assets": [
    {
      "asset_type": "stock",
      "symbol": "AAPL",
      "amount": 100
    }
  ],
  "bank_accounts": [
    {
      "institution_id": 1,
      "balance": 50000.0,
      "currency": "USD",
      "iban": "US1234567890123456"
    }
  ],
  "transactions": [...],
  "spending": [...],
  "derivatives": [...]
}
```

#### GET /bank/status
Check dummy bank connection status.

**Response:**
```json
{
  "status": "connected",
  "url": "http://localhost:3000",
  "timestamp": "2025-07-20T10:30:00"
}
```

#### GET /bank/customers
Get all customers from dummy bank (admin endpoint).

**Response:**
```json
{
  "customers": [
    {
      "customer_oid": "550e8400-e29b-41d4-a716-446655440001",
      "name": "John Doe"
    }
  ]
}
```

#### POST /bank/sync
Sync current user with dummy bank.

**Response:**
```json
{
  "message": "Successfully synced with dummy bank",
  "customer_oid": "550e8400-e29b-41d4-a716-446655440001"
}
```

### MCP Integration

#### GET /mcp/status
Get MCP server status.

**Response:**
```json
{
  "status": "connected",
  "url": "http://localhost:8001",
  "timestamp": "2025-07-20T10:30:00"
}
```

#### POST /mcp/query
Query MCP agent with natural language.

**Request Body:**
```json
{
  "query": "What is my account balance?"
}
```

**Response:**
```json
{
  "response": "Your checking account balance is $5,000.00",
  "timestamp": "2025-07-20T10:30:00",
  "status": "success"
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
  "database": "connected",
  "mcp_server": {
    "status": "connected",
    "url": "http://localhost:8001"
  },
  "dummy_bank": {
    "status": "connected", 
    "url": "http://localhost:3000"
  }
}
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
    "customer_oid": "550e8400-e29b-41d4-a716-446655440001",
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

## Dummy Bank Integration

The system integrates with a dummy bank API for:
- Customer registration with CustomerOID linking
- Portfolio data retrieval (assets, accounts, transactions)
- Account synchronization
- Connection health monitoring

## Authentication Notes

### Cookie Security
- HTTP-only cookies prevent XSS attacks
- SameSite=lax prevents CSRF attacks
- Secure flag should be enabled for HTTPS in production

### Token Management
- Bearer tokens expire in 30 minutes (configurable)
- Cookies have the same expiration as tokens
- Both authentication methods can be used simultaneously

### Flexible Authentication
The API automatically detects authentication method:
1. Checks for `Authorization: Bearer` header first
2. Falls back to HTTP-only cookie if no Bearer token
3. Returns 401 if neither method provides valid credentials
