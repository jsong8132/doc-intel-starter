"""
Invoice Agent - Extracts detailed data from invoices.

Called after router_agent classifies a document as an invoice.

Usage:
    from invoice_agent import InvoiceAgent
    
    agent = InvoiceAgent()
    result = agent.extract("invoice text content")
    print(result)
"""

import json
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()


class InvoiceAgent:
    """Extracts structured data from invoice documents."""
    
    def __init__(self):
        self.client = Anthropic()
        self.model = "claude-sonnet-4-20250514"
        self.prompt_version = "v1"
        
    def extract(self, document_text: str) -> dict:
        """
        Extract detailed invoice data.
        
        Args:
            document_text: Text content of the invoice
            
        Returns:
            dict with invoice fields (None for missing fields)
        """
        
        system_prompt = """You are an invoice data extraction agent for a property development company.

Extract all invoice details into structured JSON. Be precise with numbers and dates.

ABN format: XX XXX XXX XXX (Australian Business Number)
Date format: YYYY-MM-DD
Currency: numeric only, no symbols (e.g., 1500.00 not $1,500.00)

You MUST respond with valid JSON only, no other text:
{
    "invoice_number": "INV-2024-001",
    "vendor_name": "Smith Constructions Pty Ltd",
    "vendor_abn": "12 345 678 901",
    "invoice_date": "2024-03-15",
    "due_date": "2024-03-29",
    "project_reference": "Balmoral Estate - Lot 42",
    "description": "Concrete slab pour and related works",
    "line_items": [
        {"description": "Concrete slab pour", "quantity": 1, "unit_price": 15000.00, "amount": 15000.00}
    ],
    "subtotal": 22000.00,
    "gst_amount": 2200.00,
    "total_inc_gst": 24200.00,
    "payment_terms": "14 days"
}

Use null for any field that cannot be determined from the document."""

        user_message = f"""Extract invoice data:

---
{document_text}
---

Respond with JSON only."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}]
        )
        
        response_text = response.content[0].text
        response_text = response_text.replace("```json", "").replace("```", "").strip()
        
        try:
            result = json.loads(response_text)
        except json.JSONDecodeError:
            result = {
                "invoice_number": None, "vendor_name": None, "vendor_abn": None,
                "invoice_date": None, "due_date": None, "project_reference": None,
                "description": None, "line_items": [], "subtotal": None,
                "gst_amount": None, "total_inc_gst": None, "payment_terms": None,
                "error": f"Failed to parse response: {response_text[:200]}"
            }
        
        result["_meta"] = {"model": self.model, "prompt_version": self.prompt_version}
        return result


if __name__ == "__main__":
    agent = InvoiceAgent()
    
    test_invoice = """
    TAX INVOICE
    
    From: Smith Concreting Pty Ltd
    ABN: 12 345 678 901
    
    To: Song Capital Group
    Date: 15 March 2024
    Invoice #: INV-2024-0847
    
    Project: Balmoral Estate - Lot 42
    
    Description                     Qty    Unit Price    Amount
    ------------------------------------------------------------
    Concrete slab pour - Stage 1     1     $15,000.00    $15,000.00
    Pump hire                        1      $2,500.00     $2,500.00
    Labour                           3      $1,500.00     $4,500.00
    ------------------------------------------------------------
    Subtotal                                             $22,000.00
    GST (10%)                                             $2,200.00
    ------------------------------------------------------------
    TOTAL (inc GST)                                      $24,200.00
    
    Payment due within 14 days.
    """
    
    result = agent.extract(test_invoice)
    print(json.dumps(result, indent=2))

