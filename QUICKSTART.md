# Quick Start Guide - MCP Banking Backend

## 🚀 Prerequisites

- Python 3.8+
- Conda environment: `openbanking-backend`
- Optional: MCP Server on port 8001
- Optional: Dummy Bank API on port 3000

## ⚡ Quick Setup

### 1. Activate Environment
```powershell
conda activate openbanking-backend
```

### 2. Start the Server
```powershell
# Using the batch file
start_server.bat

# Or manually
python main.py
```

### 3. Verify Installation
```powershell
# Check server health (includes all service statuses)
curl http://localhost:8000/health

# Run comprehensive tests
python test_server.py

# Test cookie authentication
python test_cookie_auth.py
```

### 4. Access Documentation
- **API Docs**: <http://localhost:8000/docs>
- **Alternative Docs**: <http://localhost:8000/redoc>
- **Health Check**: <http://localhost:8000/health>

## 🔑 Authentication Quick Test

### Using Bearer Tokens (API Clients)
```bash
# Login and get token
curl -X POST "http://localhost:8000/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=john_doe&password=password123"

# Use token
curl -H "Authorization: Bearer <your-token>" \
     "http://localhost:8000/me"
```

### Using HTTP-Only Cookies (Web Browsers)
```bash
# Login with JSON (sets cookie)
curl -c cookies.txt -X POST "http://localhost:8000/login" \
     -H "Content-Type: application/json" \
     -d '{"username": "john_doe", "password": "password123"}'

# Use cookie
curl -b cookies.txt "http://localhost:8000/me"
```

## 🏦 Banking Operations Quick Test

```bash
# Get accounts
curl -H "Authorization: Bearer <token>" \
     "http://localhost:8000/accounts"

# Get account balance
curl -H "Authorization: Bearer <token>" \
     "http://localhost:8000/accounts/ACC001/balance"

# Transfer money
curl -X POST "http://localhost:8000/transfer?from_account_id=ACC001" \
     -H "Authorization: Bearer <token>" \
     -H "Content-Type: application/json" \
     -d '{
       "to_account_id": "ACC002",
       "amount": 100.0,
       "currency": "USD",
       "description": "Test transfer"
     }'
```

## 🏛️ Bank Integration Quick Test

```bash
# Get portfolio from dummy bank
curl -H "Authorization: Bearer <token>" \
     "http://localhost:8000/bank/portfolio"

# Check bank connection
curl -H "Authorization: Bearer <token>" \
     "http://localhost:8000/bank/status"

# Sync with dummy bank
curl -X POST -H "Authorization: Bearer <token>" \
     "http://localhost:8000/bank/sync"
```

## 🤖 MCP Integration Quick Test

```bash
# Check MCP server status
curl -H "Authorization: Bearer <token>" \
     "http://localhost:8000/mcp/status"

# Query MCP agent
curl -X POST "http://localhost:8000/mcp/query" \
     -H "Authorization: Bearer <token>" \
     -H "Content-Type: application/json" \
     -d '{"query": "What is my account balance?"}'
```

## 👤 Default Test Users

- **Username**: `john_doe` | **Password**: `password123`
- **Username**: `jane_smith` | **Password**: `password123`

## 🔧 Configuration

### Database Reset
```bash
# Reset database with dummy bank integration
python reset_database.py
```

### MCP Server Configuration
```bash
# Update MCP server URL
curl -X POST "http://localhost:8000/config" \
     -H "Authorization: Bearer <token>" \
     -H "Content-Type: application/json" \
     -d '{"mcp_server_url": "http://localhost:8001"}'
```

### Cookie Security (Production)
```python
# In auth.py for HTTPS production:
secure=True  # Enable secure flag for cookies
```

## 📊 Available Endpoints Summary

### Authentication
- `POST /register` - Register user + sync with dummy bank
- `POST /token` - Login (form-data) + set cookie
- `POST /login` - Login (JSON) + set cookie
- `POST /logout` - Clear cookie

### Banking
- `GET /accounts` - List user accounts
- `GET /accounts/{id}` - Account details
- `GET /accounts/{id}/balance` - Account balance
- `GET /accounts/{id}/transactions` - Transaction history
- `POST /transfer` - Money transfer

### Bank Integration
- `GET /bank/portfolio` - User portfolio from dummy bank
- `GET /bank/status` - Dummy bank connection status
- `GET /bank/customers` - All bank customers (admin)
- `POST /bank/sync` - Sync user with dummy bank

### MCP Integration
- `GET /mcp/status` - MCP server status
- `POST /mcp/query` - Natural language queries

### System
- `GET /health` - System health + all service statuses
- `GET /me` - Current user info
- `GET /admin/users` - All users (admin)
- `POST /config` - Update configuration

## 🧪 Testing Scripts

### Comprehensive Testing
```bash
python test_server.py          # Full authentication & banking tests
python test_cookie_auth.py     # Cookie authentication tests
```

### Database Management
```bash
python reset_database.py       # Reset DB + create sample data
```

## 🐛 Troubleshooting

### Server Not Starting
```bash
# Check if port 8000 is in use
netstat -an | findstr 8000

# Check environment
conda list fastapi
```

### Authentication Issues
```bash
# Verify user exists
curl "http://localhost:8000/admin/users"

# Check token format
echo "<your-token>" | base64 -d
```

### External Service Issues
```bash
# Check MCP server (optional)
curl http://localhost:8001/mcp/status

# Check dummy bank (optional)  
curl http://localhost:3000/health
```

## 📚 Next Steps

1. **Review API Reference**: See `API_REFERENCE.md` for complete endpoint documentation
2. **Read Main README**: See `README.md` for comprehensive project information
3. **Explore Integration**: Test with MCP server and dummy bank APIs
4. **Production Setup**: Configure HTTPS, secure cookies, and environment variables

## 💡 Pro Tips

- **Postman**: Both authentication methods work automatically
- **Web Development**: Use cookies for browser-based applications
- **API Integration**: Use Bearer tokens for server-to-server communication
- **Security**: HTTP-only cookies prevent XSS attacks
- **Flexibility**: Both auth methods can be used simultaneously
