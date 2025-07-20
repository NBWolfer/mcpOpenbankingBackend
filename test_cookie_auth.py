"""
Cookie Authentication Test Script
Demonstrates how to test HTTP-only cookie authentication with both the test script and Postman
"""

import asyncio
import httpx

BACKEND_URL = "http://localhost:8000"

async def test_cookie_authentication():
    """Test cookie-based authentication"""
    print("🍪 Testing HTTP-Only Cookie Authentication\n")
    
    # Test credentials
    username = "john_doe"
    password = "password123"
    
    # Use a session to maintain cookies
    async with httpx.AsyncClient(timeout=10.0) as client:
        
        print("1. Testing login with JSON (sets HTTP-only cookie):")
        login_response = await client.post(
            f"{BACKEND_URL}/login",
            json={
                "username": username,
                "password": password
            }
        )
        
        if login_response.status_code == 200:
            token_data = login_response.json()
            access_token = token_data["access_token"]
            print(f"   ✅ Login successful")
            print(f"   🔑 Token: {access_token[:20]}...")
            
            # Check if cookie was set
            cookies = login_response.cookies
            if "access_token" in cookies:
                print(f"   🍪 Cookie set: access_token")
                print(f"   🍪 Cookie value: {cookies['access_token'][:20]}...")
            else:
                print(f"   ⚠️ No cookie found in response")
            
        else:
            print(f"   ❌ Login failed: {login_response.status_code} - {login_response.text}")
            return
        
        print()
        
        print("2. Testing authenticated endpoint with cookie:")
        # The cookie should be automatically included in subsequent requests
        me_response = await client.get(f"{BACKEND_URL}/me")
        
        if me_response.status_code == 200:
            user_info = me_response.json()
            print(f"   ✅ Authenticated successfully via cookie")
            print(f"   👤 User: {user_info.get('full_name')} ({user_info.get('username')})")
            print(f"   🏛️ Customer OID: {user_info.get('customer_oid', 'None')}")
        else:
            print(f"   ❌ Authentication failed: {me_response.status_code} - {me_response.text}")
        
        print()
        
        print("3. Testing other endpoints with cookie:")
        
        # Test accounts endpoint
        accounts_response = await client.get(f"{BACKEND_URL}/accounts")
        if accounts_response.status_code == 200:
            accounts_data = accounts_response.json()
            accounts = accounts_data.get("accounts", [])
            print(f"   ✅ Accounts: Found {len(accounts)} accounts")
            for account in accounts:
                print(f"      - {account.get('account_name')}: ${account.get('balance'):,.2f}")
        else:
            print(f"   ❌ Accounts failed: {accounts_response.status_code}")
        
        print()
        
        print("4. Testing logout (clears cookie):")
        logout_response = await client.post(f"{BACKEND_URL}/logout")
        
        if logout_response.status_code == 200:
            logout_data = logout_response.json()
            print(f"   ✅ Logout successful: {logout_data.get('message')}")
        else:
            print(f"   ❌ Logout failed: {logout_response.status_code}")
        
        print()
        
        print("5. Testing endpoint after logout (should fail):")
        me_after_logout = await client.get(f"{BACKEND_URL}/me")
        
        if me_after_logout.status_code == 401:
            print(f"   ✅ Correctly rejected: {me_after_logout.status_code}")
        else:
            print(f"   ❌ Unexpected response: {me_after_logout.status_code}")
        
        print()
        
        print("6. Testing Bearer token authentication (should still work):")
        # Login again to get a token
        login_again = await client.post(
            f"{BACKEND_URL}/login",
            json={"username": username, "password": password}
        )
        
        if login_again.status_code == 200:
            token = login_again.json()["access_token"]
            
            # Test with Bearer token header
            headers = {"Authorization": f"Bearer {token}"}
            bearer_response = await client.get(f"{BACKEND_URL}/me", headers=headers)
            
            if bearer_response.status_code == 200:
                user_info = bearer_response.json()
                print(f"   ✅ Bearer token works: {user_info.get('username')}")
            else:
                print(f"   ❌ Bearer token failed: {bearer_response.status_code}")
        
        print("\n🎉 Cookie authentication test completed!")

def print_postman_instructions():
    """Print instructions for testing with Postman"""
    print("\n" + "="*60)
    print("📮 POSTMAN TESTING INSTRUCTIONS")
    print("="*60)
    
    print("\n1. LOGIN WITH COOKIES:")
    print("   Method: POST")
    print("   URL: http://localhost:8000/login")
    print("   Headers: Content-Type: application/json")
    print("   Body (JSON):")
    print("   {")
    print('     "username": "john_doe",')
    print('     "password": "password123"')
    print("   }")
    print("   ✅ Cookie will be automatically set by Postman")
    
    print("\n2. TEST AUTHENTICATED ENDPOINTS:")
    print("   Method: GET")
    print("   URL: http://localhost:8000/me")
    print("   Headers: (none needed - cookie automatic)")
    print("   ✅ Cookie will be automatically sent by Postman")
    
    print("\n3. ALTERNATIVE - BEARER TOKEN:")
    print("   Method: GET")
    print("   URL: http://localhost:8000/me")
    print("   Headers: Authorization: Bearer <token_from_login_response>")
    print("   ✅ Both methods work simultaneously")
    
    print("\n4. LOGOUT:")
    print("   Method: POST")
    print("   URL: http://localhost:8000/logout")
    print("   ✅ Cookie will be cleared")
    
    print("\n5. CHECK COOKIES IN POSTMAN:")
    print("   - Click 'Cookies' link below the Send button")
    print("   - Look for 'access_token' cookie for localhost:8000")
    print("   - HttpOnly flag should be set")
    
    print("\n💡 TIPS:")
    print("   - Postman automatically handles HttpOnly cookies")
    print("   - Both Bearer tokens and cookies work")
    print("   - Use cookies for web browsers, Bearer for API clients")
    print("   - Cookies are more secure (HttpOnly prevents XSS)")

if __name__ == "__main__":
    print("🏦 Banking Backend Cookie Authentication Test")
    print("Make sure the backend server is running on http://localhost:8000\n")
    
    asyncio.run(test_cookie_authentication())
    print_postman_instructions()
