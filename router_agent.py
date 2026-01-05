"""
Router Agent - Classifies documents into types.

This is the first agent. It looks at a document and decides:
- What type is it? (invoice, progress_claim, contract, variation, settlement)
- Who is the vendor?
- Which project does it relate to?
- How confident is it?

Usage:
    from router_agent import RouterAgent
    
    agent = RouterAgent()
    result = agent.classify("text content of document")
    print(result)
"""

import os
import json
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()


class RouterAgent:
    """Classifies documents and extracts basic metadata."""
    
    # The document types we care about
    DOCUMENT_TYPES = [
        "invoice",
        "progress_claim", 
        "contract",
        "variation",
        "settlement",
        "unknown"
    ]
    
    def __init__(self):
        self.client = Anthropic()
        self.model = "claude-sonnet-4-20250514"
        self.prompt_version = "v1"  # Track this for evaluation
        
    def classify(self, document_text: str) -> dict:
        """
        Classify a document and extract metadata.
        
        Args:
            document_text: The text content of the document
            
        Returns:
            dict with keys:
                - document_type: one of DOCUMENT_TYPES
                - confidence: float 0-1
                - vendor_name: str or None
                - project_name: str or None  
                - document_date: str or None
                - amount: float or None
                - reasoning: str explaining the classification
        """
        
        system_prompt = """You are a document classification agent for a property development company.

Your job is to look at a document and determine:
1. What TYPE of document is it?
2. Key metadata you can extract from it

Document types:
- invoice: A bill requesting payment for goods/services
- progress_claim: A claim from a contractor for completed work stages
- contract: A formal agreement between parties
- variation: A change order or amendment to existing contract
- settlement: Property settlement statement
- unknown: Cannot determine

Confidence scoring:
- 0.9+ : Document explicitly states its type (e.g., "TAX INVOICE" header)
- 0.7-0.9 : Strongly implied by format and content
- 0.5-0.7 : Reasonable guess based on content
- Below 0.5 : Uncertain, might need human review

You MUST respond with valid JSON only, no other text. Use this exact structure:
{
    "document_type": "invoice",
    "confidence": 0.95,
    "vendor_name": "Smith Constructions Pty Ltd",
    "project_name": "Balmoral Estate",
    "document_date": "2024-03-15",
    "amount": 24750.00,
    "reasoning": "Document has TAX INVOICE header, ABN, GST breakdown..."
}

If a field cannot be determined, use null."""

        user_message = f"""Classify this document:

---
{document_text}
---

Respond with JSON only."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}]
        )
        
        # Parse the response
        response_text = response.content[0].text
        
        try:
            result = json.loads(response_text)
        except json.JSONDecodeError:
            # If Claude didn't return valid JSON, wrap the error
            result = {
                "document_type": "unknown",
                "confidence": 0.0,
                "vendor_name": None,
                "project_name": None,
                "document_date": None,
                "amount": None,
                "reasoning": f"Failed to parse response: {response_text[:200]}"
            }
        
        # Add metadata for tracking
        result["_meta"] = {
            "model": self.model,
            "prompt_version": self.prompt_version
        }
        
        return result


# Quick test if running directly
if __name__ == "__main__":
    agent = RouterAgent()
    
    test_doc = """
    TAX INVOICE
    
    From: Smith Concreting Pty Ltd
    ABN: 12 345 678 901
    
    To: Song Capital Group
    Date: 15 March 2024
    Invoice #: INV-2024-0847
    
    Project: Balmoral Estate - Lot 42
    
    Description                     Amount
    -----------------------------------------
    Concrete slab pour - Stage 1    $15,000.00
    Pump hire                        $2,500.00
    Labour (3 days)                  $4,500.00
    -----------------------------------------
    Subtotal                        $22,000.00
    GST (10%)                        $2,200.00
    -----------------------------------------
    TOTAL                           $24,200.00
    
    Payment due within 14 days.
    Bank: NAB BSB: 083-004 Account: 12-345-6789
    """
    
    result = agent.classify(test_doc)
    print(json.dumps(result, indent=2))
