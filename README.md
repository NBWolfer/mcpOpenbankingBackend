# MCP Banking Backend with Database & Authentication

A secure FastAPI backend with SQLite database, JWT authentication, and MCP agent integration for banking operations.

## 🏗️ Architecture

```
App → Backend (Auth + DB) → MCP Server → Banking Agents (LLM/Models)
```

- **App**: Frontend application making authenticated HTTP requests
- **Backend**: FastAPI server with SQLite database and JWT authentication
- **MCP Server**: Manages banking agents and AI tools
- **Agents**: LLM/Models handling banking operations, fraud detection, etc.

## ✨ Features

- � **JWT Authentication**: Secure user authentication
- 💾 **SQLite Database**: User accounts, transactions, and banking data
- 🏦 **Banking Operations**: Account management, transfers, transaction history
- 🤖 **MCP Integration**: AI-powered banking agents and fraud detection
- 📊 **Real-time Data**: Live account balances and transaction tracking
- 🛡️ **Authorization**: Protected endpoints with user ownership validation

## �🚀 Quick Start

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
   - Server: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Database is auto-created with sample data

## 🔑 Authentication

### Default Test Users
- **Username**: `john_doe` | **Password**: `password123`
- **Username**: `jane_smith` | **Password**: `password123`

### Get Access Token
```bash
curl -X POST "http://localhost:8000/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=john_doe&password=password123"
```

## 📋 API Endpoints

### Authentication
- `POST /register` - Register new user
- `POST /token` - Login and get access token

### User & Account Management  
- `GET /me` - Get current user info
- `GET /accounts` - Get user's accounts
- `GET /accounts/{account_id}` - Get account details
- `GET /accounts/{account_id}/balance` - Get account balance
- `GET /accounts/{account_id}/transactions` - Get transaction history

### Banking Operations
- `POST /transfer?from_account_id={id}` - Transfer money between accounts

### Admin
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

## 🗄️ Database Schema

### Users Table
- `id`, `username`, `email`, `hashed_password`, `full_name`, `is_active`, `created_at`

### Accounts Table  
- `id`, `account_name`, `account_type`, `balance`, `currency`, `user_id`, `is_active`, `created_at`

### Transactions Table
- `id`, `from_account_id`, `to_account_id`, `amount`, `currency`, `description`, `transaction_type`, `status`, `created_at`

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

## 🧪 Testing

Run the comprehensive test suite:
```bash
python test_server.py
```

This will test:
- Authentication flow
- Account operations
- Money transfers
- User registration

## 📁 Project Structure

```
mcpOpenbankingBackend/
├── main.py              # Main FastAPI application
├── database.py          # SQLAlchemy models and database setup
├── auth.py              # Authentication and JWT utilities
├── schemas.py           # Pydantic request/response models
├── test_server.py       # Comprehensive test suite
├── requirements.txt     # Python dependencies
├── start_server.bat     # Easy startup script
└── banking.db          # SQLite database (auto-created)
```

## 🔧 Configuration

- **JWT Secret**: Change `SECRET_KEY` in `auth.py` for production
- **Database**: SQLite file `banking.db` (automatically created)
- **MCP Server**: Configure URL via `/config` endpoint (default: localhost:8080)

## 🛡️ Security Features

- Password hashing with bcrypt
- JWT token-based authentication
- User ownership validation for all operations
- Protected endpoints with dependency injection
- Automatic database relationship enforcement
