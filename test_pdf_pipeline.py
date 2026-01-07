from pdf_utils import extract_text
from router_agent import RouterAgent
from invoice_agent import InvoiceAgent
import json

# Step 1: Extract text from PDF
text = extract_text('Invoice INV-0911.pdf')
print("=== Extracted Text ===")
print(text[:500])  # First 500 chars

# Step 2: Classify with router
print("\n=== Router Classification ===")
router = RouterAgent()
router_result = router.classify(text)
print(json.dumps(router_result, indent=2))

# Step 3: Extract invoice details (only if it's an invoice)
if router_result.get("document_type") == "invoice":
    print("\n=== Invoice Extraction ===")
    invoice_agent = InvoiceAgent()
    extraction = invoice_agent.extract(text)
    print(json.dumps(extraction, indent=2))
else:
    print(f"\nSkipping invoice extraction - document is: {router_result.get('document_type')}")