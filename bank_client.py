"""
Bank Client for communicating with Dummy Bank API
Handles customer registration, account creation, and banking operations
"""

import httpx
import logging
from typing import Dict, Optional, Any, List
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

class DummyBankClient:
    """Client for communicating with the dummy bank API"""
    
    def __init__(self, bank_api_url: str = "http://127.0.0.1:3000"):
        self.bank_api_url = bank_api_url
        self.timeout = 10.0
    
    async def register_customer(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Register a new customer in the dummy bank"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # Map our data to dummy bank API format
                request_data = {
                    "name": customer_data.get("full_name") or customer_data.get("username"),
                    "customer_oid": str(uuid.uuid4())  # Generate UUID for the customer
                }
                
                logger.info(f"Registering customer in dummy bank: {request_data['name']}")
                response = await client.post(
                    f"{self.bank_api_url}/register-customer",
                    json=request_data,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code in [200, 201]:
                    result = response.json()
                    logger.info(f"Customer registered successfully: {result}")
                    return {
                        "status": "success", 
                        "data": result,
                        "customer_oid": result.get("customer_oid")
                    }
                else:
                    logger.error(f"Failed to register customer: {response.status_code} - {response.text}")
                    return {
                        "status": "error", 
                        "error": f"Bank API error: {response.status_code}",
                        "details": response.text
                    }
                    
        except Exception as e:
            logger.error(f"Error communicating with dummy bank: {e}")
            return {"status": "error", "error": str(e)}
    
    async def get_customer_portfolio(self, customer_oid: str) -> Dict[str, Any]:
        """Get comprehensive customer portfolio from dummy bank"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.bank_api_url}/user-portfolio/{customer_oid}")
                
                if response.status_code == 200:
                    result = response.json()
                    return {"status": "success", "data": result}
                elif response.status_code == 404:
                    return {"status": "not_found", "error": "Customer not found"}
                else:
                    return {
                        "status": "error", 
                        "error": f"Bank API error: {response.status_code}",
                        "details": response.text
                    }
                    
        except Exception as e:
            logger.error(f"Error getting portfolio from dummy bank: {e}")
            return {"status": "error", "error": str(e)}
    
    async def check_customer_exists(self, customer_oid: str) -> Dict[str, Any]:
        """Check if customer exists in dummy bank"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.bank_api_url}/customer/{customer_oid}/exists")
                
                if response.status_code == 200:
                    result = response.json()
                    return {"status": "success", "data": result}
                elif response.status_code == 404:
                    return {"status": "not_found", "exists": False}
                else:
                    return {
                        "status": "error", 
                        "error": f"Bank API error: {response.status_code}",
                        "details": response.text
                    }
                    
        except Exception as e:
            logger.error(f"Error checking customer existence: {e}")
            return {"status": "error", "error": str(e)}
    
    async def get_all_customers(self) -> Dict[str, Any]:
        """Get all customers from dummy bank"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.bank_api_url}/customers")
                
                if response.status_code == 200:
                    result = response.json()
                    return {"status": "success", "data": result}
                else:
                    return {
                        "status": "error", 
                        "error": f"Bank API error: {response.status_code}",
                        "details": response.text
                    }
                    
        except Exception as e:
            logger.error(f"Error getting customers from dummy bank: {e}")
            return {"status": "error", "error": str(e)}
    
    async def delete_customer(self, customer_oid: str) -> Dict[str, Any]:
        """Delete customer from dummy bank"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.delete(f"{self.bank_api_url}/customer/{customer_oid}")
                
                if response.status_code == 200:
                    result = response.json()
                    logger.info(f"Customer deleted successfully: {result}")
                    return {"status": "success", "data": result}
                elif response.status_code == 404:
                    return {"status": "not_found", "error": "Customer not found"}
                else:
                    return {
                        "status": "error", 
                        "error": f"Bank API error: {response.status_code}",
                        "details": response.text
                    }
                    
        except Exception as e:
            logger.error(f"Error deleting customer from dummy bank: {e}")
            return {"status": "error", "error": str(e)}
    
    async def check_connection(self) -> Dict[str, Any]:
        """Check if dummy bank API is available"""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.bank_api_url}/health")
                
                if response.status_code == 200:
                    result = response.json()
                    return {"status": "connected", "data": result}
                else:
                    return {"status": "error", "error": f"HTTP {response.status_code}"}
                    
        except Exception as e:
            return {"status": "disconnected", "error": str(e)}