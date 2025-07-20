"""
Test script for the MCP Banking Backend with Authentication
"""

import asyncio
import httpx

BASE_URL = "http://localhost:8000"

# Test credentials (these are created automatically when server starts)
TEST_USERNAME = "john_doe"
TEST_PASSWORD = "password123"

async def get_access_token() -> str:
    """Get access token for testing"""
    async with httpx.AsyncClient() as client:
        # Login to get token
        login_data = {
            "username": TEST_USERNAME,
            "password": TEST_PASSWORD
        }
        response = await client.post(f"{BASE_URL}/token", data=login_data)
        if response.status_code == 200:
            token_data = response.json()
            return token_data["access_token"]
        else:
            print(f"Login failed: {response.status_code} - {response.text}")
            return None

async def test_endpoints():
    """Test all banking endpoints with authentication"""
    # Use a longer timeout for the test client to handle MCP calls
    timeout = httpx.Timeout(30.0, read=30.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        print("🏦 Testing MCP Banking Backend with Authentication\n")
        
        # Health check (no auth required)
        print("1. Health Check:")
        response = await client.get(f"{BASE_URL}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}\n")
        
        # Get access token
        print("2. Getting Access Token:")
        token = await get_access_token()
        if not token:
            print("   ❌ Failed to get access token. Make sure server is running and sample data is loaded.")
            return
        
        print(f"   ✅ Token obtained: {token[:20]}...\n")
        
        # Set authorization header
        headers = {"Authorization": f"Bearer {token}"}
        
        # Get user info
        print("3. Get Current User Info:")
        response = await client.get(f"{BASE_URL}/me", headers=headers)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}\n")
        
        # Get accounts
        print("4. Get User Accounts:")
        response = await client.get(f"{BASE_URL}/accounts", headers=headers)
        print(f"   Status: {response.status_code}")
        data = response.json()
        print(f"   Response: {data}\n")
        
        # If accounts exist, test with first account
        if response.status_code == 200 and data.get("accounts"):
            account_id = data["accounts"][0]["id"]
            
            # Get account balance
            print(f"5. Get Account Balance (Account: {account_id}):")
            response = await client.get(f"{BASE_URL}/accounts/{account_id}/balance", headers=headers)
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}\n")
            
            # Get transactions
            print(f"6. Get Account Transactions (Account: {account_id}):")
            response = await client.get(f"{BASE_URL}/accounts/{account_id}/transactions", headers=headers)
            print(f"   Status: {response.status_code}")
            transactions = response.json()
            print(f"   Response: Found {len(transactions) if isinstance(transactions, list) else 0} transactions\n")
            
            # Test transfer (if multiple accounts exist)
            if len(data["accounts"]) > 1:
                to_account_id = data["accounts"][1]["id"]
                print(f"7. Transfer Money ({account_id} -> {to_account_id}):")
                transfer_data = {
                    "to_account_id": to_account_id,
                    "amount": 10.00,
                    "currency": "USD",
                    "description": "Test transfer"
                }
                response = await client.post(
                    f"{BASE_URL}/transfer?from_account_id={account_id}", 
                    json=transfer_data, 
                    headers=headers
                )
                print(f"   Status: {response.status_code}")
                print(f"   Response: {response.json()}\n")
        
        # Test registration (create a new user)
        print("8. Test User Registration:")
        new_user_data = {
            "username": "test_user",
            "email": "test@example.com",
            "password": "testpass123",
            "full_name": "Test User"
        }
        response = await client.post(f"{BASE_URL}/register", json=new_user_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ User registered successfully")
        elif response.status_code == 400:
            print(f"   ℹ️  User might already exist: {response.json()}")
        print()

if __name__ == "__main__":
    print("Make sure the server is running on http://localhost:8000")
    print("Start it with: python main.py\n")
    print("Default test credentials:")
    print(f"Username: {TEST_USERNAME}")
    print(f"Password: {TEST_PASSWORD}\n")
    asyncio.run(test_endpoints())
