"""
Example extensions for the MCP OpenBanking Backend
This file demonstrates how to add custom MCP methods and endpoints
"""

from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from fastapi import HTTPException
from pydantic import BaseModel

class CustomerKYCRequest(BaseModel):
    """Request model for KYC operations"""
    customer_id: str
    verification_type: str = "full"  # full, basic, enhanced
    include_documents: bool = False

class CreditScoreRequest(BaseModel):
    """Request model for credit score operations"""
    customer_id: str
    bureau: Optional[str] = None  # experian, equifax, transunion
    purpose: str = "lending"

class FraudCheckRequest(BaseModel):
    """Request model for fraud detection"""
    transaction_id: Optional[str] = None
    account_id: Optional[str] = None
    amount: Optional[float] = None
    merchant: Optional[str] = None
    location: Optional[Dict[str, Any]] = None

# Example of how to add these endpoints to the main FastAPI app
# Add these to main.py after the existing endpoints

async def add_extended_endpoints(app, mcp_client):
    """
    Function to add extended endpoints to the FastAPI app
    Call this function in main.py to include these endpoints
    """
    
    @app.post("/kyc/verify")
    async def verify_customer_kyc(
        request: CustomerKYCRequest,
        client=mcp_client
    ):
        """
        Perform KYC verification for a customer
        """
        params = {
            "customer_id": request.customer_id,
            "verification_type": request.verification_type,
            "include_documents": request.include_documents
        }
        
        try:
            result = await client.call_mcp_method("verify_kyc", params)
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/kyc/{customer_id}/status")
    async def get_kyc_status(
        customer_id: str,
        client=mcp_client
    ):
        """
        Get KYC verification status for a customer
        """
        try:
            result = await client.call_mcp_method("get_kyc_status", {"customer_id": customer_id})
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/credit-score/request")
    async def request_credit_score(
        request: CreditScoreRequest,
        client=mcp_client
    ):
        """
        Request credit score for a customer
        """
        params = {
            "customer_id": request.customer_id,
            "purpose": request.purpose
        }
        
        if request.bureau:
            params["bureau"] = request.bureau
            
        try:
            result = await client.call_mcp_method("request_credit_score", params)
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/fraud/check")
    async def check_fraud(
        request: FraudCheckRequest,
        client=mcp_client
    ):
        """
        Perform fraud detection check
        """
        params = {}
        
        if request.transaction_id:
            params["transaction_id"] = request.transaction_id
        if request.account_id:
            params["account_id"] = request.account_id
        if request.amount:
            params["amount"] = request.amount
        if request.merchant:
            params["merchant"] = request.merchant
        if request.location:
            params["location"] = request.location
            
        try:
            result = await client.call_mcp_method("fraud_check", params)
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/compliance/aml/{customer_id}")
    async def aml_check(
        customer_id: str,
        client=mcp_client
    ):
        """
        Perform Anti-Money Laundering (AML) check
        """
        try:
            result = await client.call_mcp_method("aml_check", {"customer_id": customer_id})
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/reports/regulatory/{report_type}")
    async def generate_regulatory_report(
        report_type: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        client=mcp_client
    ):
        """
        Generate regulatory compliance reports
        """
        params = {"report_type": report_type}
        
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        else:
            # Default to current month
            now = datetime.now()
            params["start_date"] = now.replace(day=1).isoformat()
            params["end_date"] = now.isoformat()
            
        try:
            result = await client.call_mcp_method("generate_regulatory_report", params)
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/loans/prequalify")
    async def loan_prequalification(
        request: Dict[str, Any],
        client=mcp_client
    ):
        """
        Perform loan pre-qualification
        """
        try:
            result = await client.call_mcp_method("loan_prequalification", request)
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/customer/{customer_id}/profile")
    async def get_customer_profile(
        customer_id: str,
        include_accounts: bool = True,
        include_transactions: bool = False,
        include_credit_info: bool = False,
        client=mcp_client
    ):
        """
        Get comprehensive customer profile
        """
        params = {
            "customer_id": customer_id,
            "include_accounts": include_accounts,
            "include_transactions": include_transactions,
            "include_credit_info": include_credit_info
        }
        
        try:
            result = await client.call_mcp_method("get_customer_profile", params)
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

# Custom MCP methods that can be called directly
CUSTOM_MCP_METHODS = {
    "verify_kyc": "Verify customer KYC status",
    "get_kyc_status": "Get current KYC verification status",
    "request_credit_score": "Request credit score from bureau",
    "fraud_check": "Perform fraud detection analysis",
    "aml_check": "Anti-Money Laundering compliance check",
    "generate_regulatory_report": "Generate compliance reports",
    "loan_prequalification": "Pre-qualify customer for loan products",
    "get_customer_profile": "Get comprehensive customer information",
    "risk_assessment": "Perform risk assessment",
    "transaction_monitoring": "Monitor transactions for suspicious activity",
    "account_reconciliation": "Reconcile account balances",
    "payment_validation": "Validate payment instructions",
    "currency_conversion": "Convert between currencies",
    "interest_calculation": "Calculate interest for accounts",
    "fee_calculation": "Calculate applicable fees",
}

# Example webhook handlers for real-time events
async def handle_transaction_webhook(payload: Dict[str, Any], client):
    """Handle incoming transaction webhooks"""
    transaction_id = payload.get("transaction_id")
    amount = payload.get("amount")
    
    # Perform real-time fraud check
    fraud_result = await client.call_mcp_method("fraud_check", {
        "transaction_id": transaction_id,
        "amount": amount,
        "real_time": True
    })
    
    # Log the result
    print(f"Fraud check for transaction {transaction_id}: {fraud_result}")
    
    return fraud_result

async def handle_account_update_webhook(payload: Dict[str, Any], client):
    """Handle account update webhooks"""
    account_id = payload.get("account_id")
    
    # Trigger account reconciliation
    reconciliation_result = await client.call_mcp_method("account_reconciliation", {
        "account_id": account_id
    })
    
    return reconciliation_result
