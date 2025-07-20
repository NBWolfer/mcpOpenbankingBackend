# MCP Banking Backend with Database & Authentication

A comprehensive FastAPI backend with SQLite database, JWT authentication, HTTP-only cookies, dummy bank integration, and MCP agent integration for secure banking operations.

## 🏗️ Architecture

```text
App → Backend (Auth + DB + Bank Client) → MCP Server → Banking Agents (LLM/Models)
                    ↓
              Dummy Bank API (Port 3000)
```

- **App**: Frontend application making authenticated HTTP requests
- **Backend**: FastAPI server with SQLite database, JWT authentication, and bank integration
- **MCP Server**: Manages banking agents and AI tools (Port 8001)
- **Dummy Bank API**: External banking system for customer portfolios (Port 3000)
- **Agents**: LLM/Models handling banking operations, fraud detection, etc.

## ✨ Features

- 🔐 **Dual Authentication**: JWT tokens + HTTP-only cookies for web security
- 💾 **SQLite Database**: User accounts, transactions, and banking data with CustomerOID linking
- 🏦 **Banking Operations**: Account management, transfers, transaction history
- 🔗 **Bank Integration**: Full dummy bank API integration with CustomerOID synchronization
- 🤖 **MCP Integration**: AI-powered banking agents and fraud detection
- 📊 **Real-time Data**: Live account balances and transaction tracking
- 🛡️ **Authorization**: Protected endpoints with user ownership validation
- 🍪 **Secure Cookies**: HTTP-only cookies for web browser authentication
- 🔄 **Auto-Sync**: Automatic customer registration with external bank systems

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- MCP Server running on port 8001 (optional)
- Dummy Bank API on port 3000 (optional)

### Installation & Setup

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Start the server:**

   ```cmd
   start_server.bat
   ```

   Or manually:

   ```bash
   python main.py
   ```

3. **Access the API:**

   - Server: <http://localhost:8000>
   - API Documentation: <http://localhost:8000/docs>
   - Health Check: <http://localhost:8000/health>
   - Database is auto-created with sample data

### First Steps

1. **Register a new user** (automatically syncs with dummy bank)
2. **Login** using `/login` or `/token` endpoint (receives HTTP-only cookie)
3. **Access protected endpoints** using Bearer token or cookies
4. **View portfolio** from integrated dummy bank via `/bank/portfolio`

## 🔑 Authentication

### Default Test Users

- **Username**: `john_doe` | **Password**: `password123`
- **Username**: `jane_smith` | **Password**: `password123`

### Authentication Methods

#### Bearer Token (API Clients)

```bash
curl -X POST "http://localhost:8000/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=john_doe&password=password123"
```

#### HTTP-Only Cookies (Web Browsers)

```bash
curl -c cookies.txt -X POST "http://localhost:8000/login" \
     -H "Content-Type: application/json" \
     -d '{"username": "john_doe", "password": "password123"}'
```

## 📋 API Endpoints

### Authentication

- `POST /register` - Register new user (with dummy bank sync)
- `POST /token` - Login with form data (sets HTTP-only cookie)
- `POST /login` - Login with JSON (sets HTTP-only cookie)
- `POST /logout` - Logout (clears HTTP-only cookie)

### User & Account Management

- `GET /me` - Get current user info
- `GET /accounts` - Get user's accounts
- `GET /accounts/{account_id}` - Get account details
- `GET /accounts/{account_id}/balance` - Get account balance
- `GET /accounts/{account_id}/transactions` - Get transaction history

### Banking Operations

- `POST /transfer?from_account_id={id}` - Transfer money between accounts

### Dummy Bank Integration

- `GET /bank/portfolio` - Get user's portfolio from dummy bank
- `GET /bank/status` - Check dummy bank connection status
- `GET /bank/customers` - Get all customers from dummy bank (admin)
- `POST /bank/sync` - Sync current user with dummy bank

### MCP Integration

- `GET /mcp/status` - Get MCP server status
- `POST /mcp/query` - Query MCP agent with natural language

### Admin & Health

- `GET /health` - System health check (includes all service statuses)
- `GET /admin/users` - Get all users
- `POST /config` - Update MCP server configuration

## 🧪 Usage Examples

### Register New User

```bash
curl -X POST "http://localhost:8000/register" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "newuser",
       "email": "user@example.com", 
       "password": "securepass123",
       "full_name": "New User"
     }'
```

### Get Account Balance (with authentication)

```bash
# First get token
TOKEN=$(curl -s -X POST "http://localhost:8000/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=john_doe&password=password123" | jq -r .access_token)

# Then get balance
curl -H "Authorization: Bearer $TOKEN" \
     "http://localhost:8000/accounts/ACC001/balance"
```

### Transfer Money

```bash
curl -X POST "http://localhost:8000/transfer?from_account_id=ACC001" \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "to_account_id": "ACC002",
       "amount": 100.00,
       "currency": "USD",
       "description": "Transfer to savings"
     }'
```

### Cookie Authentication (Web Browsers)

```bash
# Login with JSON and receive HTTP-only cookie
curl -c cookies.txt -X POST "http://localhost:8000/login" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "john_doe",
       "password": "password123"
     }'

# Use cookie for subsequent requests
curl -b cookies.txt "http://localhost:8000/me"

# Logout (clears cookie)
curl -b cookies.txt -c cookies.txt -X POST "http://localhost:8000/logout"
```

### Bank Integration Examples

```bash
# Get user's portfolio from dummy bank
curl -H "Authorization: Bearer $TOKEN" \
     "http://localhost:8000/bank/portfolio"

# Sync current user with dummy bank
curl -X POST "http://localhost:8000/bank/sync" \
     -H "Authorization: Bearer $TOKEN"

# Check dummy bank connection
curl -H "Authorization: Bearer $TOKEN" \
     "http://localhost:8000/bank/status"
```

## 🗄️ Database Schema

### Users Table

- `id`, `username`, `email`, `hashed_password`, `full_name`, `customer_oid`, `is_active`, `created_at`

### Accounts Table

- `id`, `account_name`, `account_type`, `balance`, `currency`, `user_id`, `is_active`, `created_at`

### Transactions Table

- `id`, `from_account_id`, `to_account_id`, `amount`, `currency`, `description`, `transaction_type`, `status`, `created_at`

**Note**: The `customer_oid` field links local users to external dummy bank customers for portfolio synchronization.

## 🤖 MCP Integration

The backend automatically notifies MCP agents about:

- Account access and balance checks
- Transaction history requests
- Money transfers and fraud detection
- User authentication events

MCP agents can provide:

- Real-time fraud detection
- Transaction categorization
- Spending analysis
- Account recommendations

## 📁 Project Structure

```text
mcpOpenbankingBackend/
├── main.py              # Main FastAPI application with dual authentication
├── database.py          # SQLAlchemy models and database setup with CustomerOID
├── auth.py              # JWT + Cookie authentication utilities
├── schemas.py           # Pydantic request/response models
├── bank_client.py       # Dummy bank API integration client
├── test_server.py       # Comprehensive test suite
├── test_cookie_auth.py  # Cookie authentication testing
├── reset_database.py    # Database reset with dummy bank sync
├── requirements.txt     # Python dependencies
├── environment.yaml     # Conda environment specification
├── start_server.bat     # Easy startup script
├── .gitignore          # Git ignore rules
└── banking.db          # SQLite database (auto-created)
```

## 🔧 Configuration

- **JWT Secret**: Change `SECRET_KEY` in `auth.py` for production
- **Database**: SQLite file `banking.db` (automatically created)
- **MCP Server**: Configured for port 8001 (update via `/config` endpoint)
- **Dummy Bank**: External API on port 3000 for portfolio data
- **Cookies**: HTTP-only, SameSite=lax (set secure=True for HTTPS in production)

## 🛡️ Security Features

- **Dual Authentication**: JWT Bearer tokens + HTTP-only cookies
- **Password Security**: bcrypt hashing with salt
- **Session Management**: Secure cookie configuration with proper flags
- **Authorization**: User ownership validation for all operations
- **Protected Endpoints**: Dependency injection for authentication
- **CORS**: Configurable for production environments
- **Database Security**: Automatic relationship enforcement and input validation
- **External API**: Secure integration with dummy bank using CustomerOID linking

## 🧪 Testing & Development

### Cookie Authentication Testing

```bash
# Run cookie authentication tests
python test_cookie_auth.py
```

### Postman Testing

The API supports both authentication methods:

- **Bearer Token**: Add `Authorization: Bearer <token>` header
- **Cookies**: Postman automatically handles cookies after login

### Database Reset

```bash
# Reset database with dummy bank integration
python reset_database.py
```

### Run Comprehensive Tests

```bash
# Run all tests
python test_server.py
```

This will test:

- Authentication flow
- Account operations
- Money transfers
- User registration
- Cookie authentication
- Bank integration

## 🚀 External Integrations

### MCP Server (Port 8001)

- Banking agent operations
- Fraud detection
- Transaction analysis
- Natural language queries

### Dummy Bank API (Port 3000)

- Customer registration with CustomerOID
- Portfolio data retrieval
- Account synchronization
- Connection health monitoring

## 📊 Health Monitoring

Access the health endpoint to check all service statuses:

```bash
curl http://localhost:8000/health
```

Returns status for:

- FastAPI backend
- SQLite database
- MCP server connection
- Dummy bank API connection

## 🔄 Development Workflow

1. **Start External Services** (optional):
   - MCP Server on port 8001
   - Dummy Bank API on port 3000

2. **Initialize Backend**:

   ```bash
   python main.py
   ```

3. **Test Authentication**:

   ```bash
   python test_cookie_auth.py
   ```

4. **Reset Database** (if needed):

   ```bash
   python reset_database.py
   ```

5. **Access API Documentation**: <http://localhost:8000/docs>

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Run tests to ensure functionality
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.
