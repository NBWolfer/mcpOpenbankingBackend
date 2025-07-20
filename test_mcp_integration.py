"""
Integration test for the MCP query endpoint
Tests the flow from React frontend to Python backend
"""

import asyncio
import httpx
import json

BASE_URL = "http://localhost:8000"

async def test_mcp_integration():
    """Test the complete MCP integration flow"""
    async with httpx.AsyncClient() as client:
        
        print("=== MCP Integration Test ===\n")
        
        # Test 1: Register a test user (if not exists)
        print("1. Setting up test user...")
        test_user = {
            "username": "mcptest",
            "email": "mcptest@example.com",
            "password": "testpass123",
            "full_name": "MCP Test User"
        }
        
        try:
            response = await client.post(f"{BASE_URL}/register", json=test_user)
            if response.status_code == 200:
                print("✅ Test user created successfully")
            elif response.status_code == 400:
                print("ℹ️  Test user already exists (OK)")
            else:
                print(f"❌ User creation failed: {response.status_code}")
        except Exception as e:
            print(f"❌ User creation error: {e}")
        
        print()
        
        # Test 2: Login and get cookie-based session
        print("2. Logging in...")
        login_data = {
            "username": "mcptest",
            "password": "testpass123"
        }
        
        try:
            response = await client.post(
                f"{BASE_URL}/login",
                data=login_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            
            if response.status_code == 200:
                print("✅ Login successful")
                # The cookie will be automatically stored in the client
                login_response = response.json()
                print(f"   Logged in as: {login_response.get('user', {}).get('username', 'Unknown')}")
            else:
                print(f"❌ Login failed: {response.status_code}")
                return
        except Exception as e:
            print(f"❌ Login error: {e}")
            return
        
        print()
        
        # Test 3: Test MCP query with different types of queries
        test_queries = [
            "Hello, can you help me?",
            "Analyze my investment portfolio",
            "What's my risk exposure?",
            "Show me portfolio recommendations"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"3.{i}. Testing MCP query: '{query}'")
            
            try:
                response = await client.post(
                    f"{BASE_URL}/mcp/query",
                    json={"query": query}
                    # Cookie is automatically included
                )
                
                if response.status_code == 200:
                    result = response.json()
                    source = result.get("source", "unknown")
                    ai_response = result.get("response", "No response")
                    
                    print(f"✅ Query successful")
                    print(f"   Agent: {source}")
                    print(f"   Response: {ai_response[:100]}..." if len(ai_response) > 100 else f"   Response: {ai_response}")
                else:
                    print(f"❌ Query failed: {response.status_code}")
                    error_detail = response.json() if response.headers.get('content-type') == 'application/json' else response.text
                    print(f"   Error: {error_detail}")
                    
            except Exception as e:
                print(f"❌ Query error: {e}")
            
            print()
        
        # Test 4: Test with invalid query
        print("4. Testing error handling...")
        try:
            response = await client.post(
                f"{BASE_URL}/mcp/query",
                json={"query": ""}  # Empty query
            )
            
            if response.status_code == 400:
                print("✅ Error handling works correctly")
                error = response.json()
                print(f"   Error message: {error.get('detail', 'Unknown error')}")
            else:
                print(f"❌ Expected 400 error, got: {response.status_code}")
        except Exception as e:
            print(f"❌ Error handling test failed: {e}")
        
        print("\n=== Integration Test Complete ===")
        print("\nTo test the frontend integration:")
        print("1. Start the Python backend: python main.py")
        print("2. Start the React frontend: npm start")
        print("3. Login with username 'mcptest' and password 'testpass123'")
        print("4. Try sending messages in the chatbot")

if __name__ == "__main__":
    print("Testing MCP Query Integration...")
    print("Make sure the Python backend is running on http://localhost:8000\n")
    
    try:
        asyncio.run(test_mcp_integration())
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    except Exception as e:
        print(f"\nTest error: {e}")
