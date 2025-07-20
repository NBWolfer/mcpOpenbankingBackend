"""
Test script for Dummy Bank Integration
Tests the communication between banking backend and dummy bank API
"""

import asyncio
import httpx

BACKEND_URL = "http://localhost:8000"
DUMMY_BANK_URL = "http://127.0.0.1:3000"
TEST_USERNAME = "bank_test_user"
TEST_PASSWORD = "password123"

async def test_dummy_bank_integration():
    """Test the dummy bank integration functionality"""
    print("🏦 Testing Dummy Bank Integration\n")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        
        # 1. Check health including dummy bank status
        print("1. Checking system health (including dummy bank status):")
        response = await client.get(f"{BACKEND_URL}/health")
        if response.status_code == 200:
            health_data = response.json()
            print(f"   ✅ Backend: {health_data.get('status')}")
            print(f"   ✅ Database: {health_data.get('database')}")
            print(f"   📡 MCP Server: {health_data.get('mcp_server', {}).get('status', 'unknown')}")
            
            dummy_bank_status = health_data.get('dummy_bank', {})
            print(f"   🏛️ Dummy Bank: {dummy_bank_status.get('status', 'unknown')}")
            if dummy_bank_status.get('status') != 'connected':
                print(f"      ⚠️ Bank Error: {dummy_bank_status.get('error', 'Unknown error')}")
                print("      Make sure dummy bank is running on http://127.0.0.1:3000")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
        print()
        
        # 2. Check dummy bank directly
        print("2. Testing direct connection to dummy bank:")
        try:
            response = await client.get(f"{DUMMY_BANK_URL}/health")
            if response.status_code == 200:
                bank_health = response.json()
                print(f"   ✅ Dummy Bank Direct: {bank_health.get('status')}")
                print(f"   🏛️ Service: {bank_health.get('service')}")
            else:
                print(f"   ❌ Dummy bank not responding: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Cannot connect to dummy bank: {e}")
            print("   Please start the dummy bank API on port 3000")
        print()
        
        # 3. Register new user (should sync with dummy bank)
        print("3. Registering new user (with dummy bank sync):")
        user_data = {
            "username": TEST_USERNAME,
            "email": f"{TEST_USERNAME}@example.com",
            "full_name": "Bank Test User",
            "password": TEST_PASSWORD
        }
        
        response = await client.post(f"{BACKEND_URL}/register", json=user_data)
        if response.status_code == 200:
            user_info = response.json()
            print(f"   ✅ User registered: {user_info.get('username')}")
            print(f"   🆔 User ID: {user_info.get('id')}")
            customer_oid = user_info.get('customer_oid')
            if customer_oid:
                print(f"   🏛️ Customer OID: {customer_oid}")
            else:
                print("   ⚠️ No Customer OID - dummy bank sync may have failed")
        else:
            print(f"   ❌ User registration failed: {response.status_code} - {response.text}")
            if "already registered" in response.text:
                print("   ℹ️ User already exists, continuing with tests...")
            else:
                return
        print()
        
        # 4. Login and get token
        print("4. Logging in to get access token:")
        login_data = {
            "username": TEST_USERNAME,
            "password": TEST_PASSWORD
        }
        response = await client.post(f"{BACKEND_URL}/token", data=login_data)
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data["access_token"]
            print(f"   ✅ Login successful")
            print(f"   🔑 Token: {access_token[:20]}...")
        else:
            print(f"   ❌ Login failed: {response.status_code}")
            return
        print()
        
        # Headers with authentication
        headers = {"Authorization": f"Bearer {access_token}"}
        
        # 5. Check bank status
        print("5. Checking dummy bank connection status:")
        response = await client.get(f"{BACKEND_URL}/bank/status", headers=headers)
        if response.status_code == 200:
            bank_status = response.json()
            print(f"   🏛️ Bank Status: {bank_status.get('status')}")
            if bank_status.get('status') != 'connected':
                print(f"   ⚠️ Bank Error: {bank_status.get('error')}")
        else:
            print(f"   ❌ Bank status check failed: {response.status_code}")
        print()
        
        # 6. Get user portfolio from dummy bank
        print("6. Getting user portfolio from dummy bank:")
        response = await client.get(f"{BACKEND_URL}/bank/portfolio", headers=headers)
        if response.status_code == 200:
            portfolio = response.json()
            print(f"   ✅ Portfolio retrieved successfully")
            print(f"   👤 Customer: {portfolio.get('user', {}).get('name', 'Unknown')}")
            
            summary = portfolio.get('portfolio_summary', {})
            print(f"   💰 Total Cash Balance: ${summary.get('total_cash_balance', 0):,.2f}")
            print(f"   📊 Total Assets: {summary.get('total_assets', 0)}")
            print(f"   🏦 Total Accounts: {summary.get('total_accounts', 0)}")
            print(f"   📋 Total Transactions: {summary.get('total_transactions', 0)}")
            
        elif response.status_code == 404:
            print(f"   ⚠️ Portfolio not found - user may not be synced with dummy bank")
            
            # Try manual sync
            print("   🔄 Attempting manual sync with dummy bank...")
            sync_response = await client.post(f"{BACKEND_URL}/bank/sync", headers=headers)
            if sync_response.status_code == 200:
                sync_result = sync_response.json()
                print(f"   ✅ Sync successful: {sync_result.get('message')}")
                print(f"   🆔 Customer OID: {sync_result.get('customer_oid')}")
            else:
                print(f"   ❌ Sync failed: {sync_response.status_code}")
        else:
            print(f"   ❌ Failed to get portfolio: {response.status_code} - {response.text}")
        print()
        
        # 7. List all customers in dummy bank
        print("7. Listing all customers in dummy bank:")
        response = await client.get(f"{BACKEND_URL}/bank/customers", headers=headers)
        if response.status_code == 200:
            customers = response.json()
            print(f"   ✅ Found {len(customers)} customers in dummy bank:")
            for customer in customers[:5]:  # Show first 5
                print(f"      - {customer.get('name')} ({customer.get('customer_oid')})")
            if len(customers) > 5:
                print(f"      ... and {len(customers) - 5} more")
        else:
            print(f"   ❌ Failed to get customers: {response.status_code}")
        print()
        
        print("🎉 Dummy bank integration test completed!")

if __name__ == "__main__":
    asyncio.run(test_dummy_bank_integration())
