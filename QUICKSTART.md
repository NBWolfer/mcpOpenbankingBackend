# Quick Setup Guide for MCP OpenBanking Backend

## 🚀 Quick Start

1. **Activate the environment:**
   ```powershell
   conda activate openbanking-backend
   ```

2. **Start the server:**
   ```powershell
   # Using PowerShell script
   .\start_server.ps1
   
   # Or manually
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

3. **Test the server:**
   ```powershell
   python test_server.py
   ```

4. **Access the API documentation:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## 📋 Available Endpoints

### Core Endpoints
- `GET /health` - Health check
- `GET /mcp/status` - MCP server status
- `POST /mcp/call` - Generic MCP method call

### Banking Operations
- `GET /accounts` - List accounts
- `GET /accounts/{account_id}` - Account details
- `POST /accounts/{account_id}/balance` - Get balance
- `POST /accounts/{account_id}/transactions` - Get transactions
- `POST /payments/initiate` - Initiate payment
- `GET /payments/{payment_id}/status` - Payment status

### Configuration
- `POST /config/mcp-server` - Update MCP server URL

## 🔧 Configuration

Edit `config.json` to configure:
- MCP server URL (default: http://localhost:8080)
- Server settings
- CORS settings

## 🧪 Testing

Test specific endpoints:
```powershell
# Health check
curl http://localhost:8000/health

# List accounts
curl "http://localhost:8000/accounts?customer_id=12345"

# Generic MCP call
curl -X POST "http://localhost:8000/mcp/call" -H "Content-Type: application/json" -d '{"method": "test", "params": {}}'
```

## 🐳 Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build and run manually
docker build -t mcp-openbanking-backend .
docker run -p 8000:8000 mcp-openbanking-backend
```

## 📝 Notes

- The server will work even if the MCP server is not available
- All MCP communication errors are handled gracefully
- Check logs for debugging information
- Extensions can be added using the `extensions.py` file
