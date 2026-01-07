"""
PDF Utilities - Extract text from PDFs using Azure Document Intelligence.

Preprocessing step before router_agent.py and invoice_agent.py.

Usage:
    from pdf_utils import extract_text
    
    text = extract_text("document.pdf")
"""

import os
import sys
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

load_dotenv()


def _get_client() -> DocumentIntelligenceClient:
    """Create and return Azure Document Intelligence client."""
    endpoint = os.getenv("AZURE_DOC_INTEL_ENDPOINT")
    key = os.getenv("AZURE_DOC_INTEL_KEY")
    if not endpoint or not key:
        raise ValueError("Missing AZURE_DOC_INTEL_ENDPOINT or AZURE_DOC_INTEL_KEY in .env")
    return DocumentIntelligenceClient(endpoint, AzureKeyCredential(key))


def extract_text(file_path: str) -> str:
    """
    Extract text from a PDF using prebuilt-read model.
    
    Args:
        file_path: Path to the PDF file
        
    Returns:
        Extracted text content as a string
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    try:
        client = _get_client()
        with open(file_path, "rb") as f:
            poller = client.begin_analyze_document("prebuilt-read", body=f)
        result = poller.result()
        
        # Combine all page content
        text_parts = []
        for page in result.pages:
            for line in page.lines or []:
                text_parts.append(line.content)
        return "\n".join(text_parts)
    
    except Exception as e:
        raise RuntimeError(f"Failed to extract text: {e}")


# TODO: Fix extract_invoice function - SDK field access issues
# def extract_invoice(file_path: str) -> dict:
#     """
#     Extract structured invoice data using prebuilt-invoice model.
#     
#     Args:
#         file_path: Path to the invoice PDF
#         
#     Returns:
#         Dict with raw_text, vendor_name, invoice_number, invoice_date,
#         total, line_items, and confidence
#     """
#     if not os.path.exists(file_path):
#         raise FileNotFoundError(f"File not found: {file_path}")
#     
#     try:
#         client = _get_client()
#         with open(file_path, "rb") as f:
#             poller = client.begin_analyze_document("prebuilt-invoice", body=f)
#         result = poller.result()
#         
#         # Extract first invoice (most common case)
#         invoice = result.documents[0] if result.documents else None
#         fields = invoice.fields if invoice else {}
#         
#         def get_field(name):
#             f = fields.get(name)
#             return f.value if hasattr(f, 'value') else (f.content if f else None)
#         
#         def get_nested_content(fields_dict, name):
#             f = fields_dict.get(name) if isinstance(fields_dict, dict) else None
#             if f and hasattr(f, 'content'):
#                 return f.content
#             return None
#         
#         def get_currency(name):
#             f = fields.get(name)
#             if f and hasattr(f, 'value') and hasattr(f.value, 'amount'):
#                 return f.value.amount
#             return None
#         
#         # Extract line items
#         line_items = []
#         items_field = fields.get("Items")
#         items_list = items_field.values if hasattr(items_field, 'values') else []
#         for item in items_list:
#             item_fields = item.value if hasattr(item, 'value') else {}
#             line_items.append({
#                 "description": get_nested_content(item_fields, "Description"),
#                 "quantity": get_nested_content(item_fields, "Quantity"),
#                 "amount": get_nested_content(item_fields, "Amount"),
#             })
#         
#         return {
#             "raw_text": result.content,
#             "vendor_name": get_field("VendorName"),
#             "invoice_number": get_field("InvoiceId"),
#             "invoice_date": get_field("InvoiceDate"),
#             "total": get_currency("InvoiceTotal"),
#             "line_items": line_items,
#             "confidence": invoice.confidence if invoice else 0.0
#         }
#     
#     except Exception as e:
#         raise RuntimeError(f"Failed to extract invoice: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pdf_utils.py <path_to_pdf>")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    print(f"Processing: {pdf_path}\n")
    
    print("=== extract_text ===")
    text = extract_text(pdf_path)
    print(text[:500] if len(text) > 500 else text)
    print(f"\n[Total: {len(text)} characters]")

