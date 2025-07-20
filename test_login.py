"""
Login Test Script
Demonstrates how to login to the banking backend
"""

import asyncio
import httpx

BACKEND_URL = "http://localhost:8000"

async def test_login_methods():
    """Test both login methods"""
    print("🔑 Testing Login Methods\n")
    
    # Test credentials from the seeded database
    test_users = [
        {"username": "john_doe", "password": "password123"},
        {"username": "jane_smith", "password": "password123"}
    ]
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        
        for user_creds in test_users:
            username = user_creds["username"]
            password = user_creds["password"]
            
            print(f"Testing login for: {username}")
            
            # Method 1: /token endpoint (OAuth2 standard - form data)
            print("  Method 1: POST /token (OAuth2 form data)")
            try:
                response = await client.post(
                    f"{BACKEND_URL}/token",
                    data={
                        "username": username,
                        "password": password
                    }
                )
                
                if response.status_code == 200:
                    token_data = response.json()
                    access_token = token_data["access_token"]
                    print(f"    ✅ Success: {access_token[:20]}...")
                else:
                    print(f"    ❌ Failed: {response.status_code} - {response.text}")
            except Exception as e:
                print(f"    ❌ Error: {e}")
            
            # Method 2: /login endpoint (JSON data)
            print("  Method 2: POST /login (JSON data)")
            try:
                response = await client.post(
                    f"{BACKEND_URL}/login",
                    json={
                        "username": username,
                        "password": password
                    }
                )
                
                if response.status_code == 200:
                    token_data = response.json()
                    access_token = token_data["access_token"]
                    print(f"    ✅ Success: {access_token[:20]}...")
                    
                    # Test the token by getting user info
                    headers = {"Authorization": f"Bearer {access_token}"}
                    me_response = await client.get(f"{BACKEND_URL}/me", headers=headers)
                    
                    if me_response.status_code == 200:
                        user_info = me_response.json()
                        print(f"    👤 User Info: {user_info.get('full_name')} ({user_info.get('username')})")
                        if user_info.get('customer_oid'):
                            print(f"    🏛️ Customer OID: {user_info.get('customer_oid')}")
                        else:
                            print(f"    ⚠️ No Customer OID found")
                    else:
                        print(f"    ❌ Failed to get user info: {me_response.status_code}")
                        
                else:
                    print(f"    ❌ Failed: {response.status_code} - {response.text}")
            except Exception as e:
                print(f"    ❌ Error: {e}")
            
            print()

if __name__ == "__main__":
    print("🏦 Banking Backend Login Test")
    print("Make sure the backend server is running on http://localhost:8000\n")
    asyncio.run(test_login_methods())
