"""
Database Reset Script with Dummy Bank Integration
Resets the local database and re-seeds it with data from dummy bank
"""

import asyncio
import httpx
import os
from database import engine, Base, SessionLocal, User, Account, Transaction
from auth import get_password_hash

async def reset_database_with_dummy_bank():
    """Reset database and initialize with dummy bank integration"""
    
    # Remove existing database file
    db_file = "banking.db"
    if os.path.exists(db_file):
        os.remove(db_file)
        print(f"✅ Removed existing database: {db_file}")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✅ Created database tables")
    
    async def register_with_dummy_bank(name: str) -> str:
        """Register customer with dummy bank and return CustomerOID"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                print(f"🏛️ Registering '{name}' with dummy bank...")
                response = await client.post(
                    "http://127.0.0.1:3000/register-customer",
                    json={"name": name},
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code in [200, 201]:
                    result = response.json()
                    customer_oid = result.get("customer_oid")
                    print(f"   ✅ Registered: {customer_oid}")
                    return customer_oid
                else:
                    print(f"   ❌ Failed: {response.status_code} - {response.text}")
                    return None
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return None
    
    # Check dummy bank connection first
    print("🏛️ Checking dummy bank connection...")
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("http://127.0.0.1:3000/health")
            if response.status_code == 200:
                health = response.json()
                print(f"   ✅ Dummy bank is running: {health.get('status')}")
            else:
                print(f"   ❌ Dummy bank health check failed: {response.status_code}")
                return
    except Exception as e:
        print(f"   ❌ Cannot connect to dummy bank: {e}")
        print("   Please make sure dummy bank is running on http://127.0.0.1:3000")
        return
    
    # Register sample users with dummy bank
    print("\n📝 Registering sample users with dummy bank...")
    john_customer_oid = await register_with_dummy_bank("John Doe")
    jane_customer_oid = await register_with_dummy_bank("Jane Smith")
    
    if not john_customer_oid or not jane_customer_oid:
        print("❌ Failed to register users with dummy bank")
        return
    
    # Create local database entries
    print("\n💾 Creating local database entries...")
    db = SessionLocal()
    try:
        # Create sample users with CustomerOIDs from dummy bank
        user1 = User(
            username="john_doe",
            email="john@example.com",
            hashed_password=get_password_hash("password123"),
            full_name="John Doe",
            customer_oid=john_customer_oid
        )
        user2 = User(
            username="jane_smith",
            email="jane@example.com", 
            hashed_password=get_password_hash("password123"),
            full_name="Jane Smith",
            customer_oid=jane_customer_oid
        )
        
        db.add(user1)
        db.add(user2)
        db.commit()
        db.refresh(user1)
        db.refresh(user2)
        
        print(f"   ✅ Created user: {user1.username} (ID: {user1.id}, CustomerOID: {john_customer_oid})")
        print(f"   ✅ Created user: {user2.username} (ID: {user2.id}, CustomerOID: {jane_customer_oid})")
        
        # Create sample accounts
        accounts = [
            Account(id="ACC001", account_name="John's Checking", account_type="checking", 
                   balance=5000.0, user_id=user1.id),
            Account(id="ACC002", account_name="John's Savings", account_type="savings", 
                   balance=15000.0, user_id=user1.id),
            Account(id="ACC003", account_name="Jane's Checking", account_type="checking", 
                   balance=3000.0, user_id=user2.id),
            Account(id="ACC004", account_name="Jane's Savings", account_type="savings", 
                   balance=8000.0, user_id=user2.id),
        ]
        
        for account in accounts:
            db.add(account)
            print(f"   ✅ Created account: {account.account_name} ({account.id})")
        
        db.commit()
        
        # Create sample transactions
        transactions = [
            Transaction(id="TXN001", from_account_id="ACC001", amount=50.0, 
                       description="ATM Withdrawal", transaction_type="withdrawal", status="completed"),
            Transaction(id="TXN002", to_account_id="ACC001", amount=1000.0, 
                       description="Salary Deposit", transaction_type="deposit", status="completed"),
            Transaction(id="TXN003", from_account_id="ACC001", to_account_id="ACC003", 
                       amount=200.0, description="Transfer to Jane", transaction_type="transfer", status="completed"),
        ]
        
        for transaction in transactions:
            db.add(transaction)
            print(f"   ✅ Created transaction: {transaction.id} ({transaction.transaction_type})")
        
        db.commit()
        
        print(f"\n🎉 Database reset and seeded successfully!")
        print(f"📊 Created:")
        print(f"   - 2 users (with dummy bank CustomerOIDs)")
        print(f"   - 4 accounts")
        print(f"   - 3 transactions")
        
        print(f"\n🔑 Test credentials:")
        print(f"   Username: john_doe | Password: password123 | CustomerOID: {john_customer_oid}")
        print(f"   Username: jane_smith | Password: password123 | CustomerOID: {jane_customer_oid}")
        
    except Exception as e:
        print(f"❌ Error creating local database entries: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🗄️ Resetting database with dummy bank integration...\n")
    asyncio.run(reset_database_with_dummy_bank())
