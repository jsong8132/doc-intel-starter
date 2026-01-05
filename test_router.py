"""
Test the Router Agent

This is a simple test script. Run it with:
    python test_router.py

Later, you'll convert this to proper pytest tests with evaluation metrics.
"""

import json
import time
from router_agent import RouterAgent


def load_sample_document(filename: str) -> str:
    """Load a sample document from file."""
    with open(filename, "r") as f:
        return f.read()


def test_router_basic():
    """Test that the router can classify a simple invoice."""
    
    print("=" * 60)
    print("TEST: Basic Invoice Classification")
    print("=" * 60)
    
    # Load the sample
    doc_text = load_sample_document("sample_invoice.txt")
    print(f"\nDocument preview:\n{doc_text[:200]}...\n")
    
    # Create agent and classify
    agent = RouterAgent()
    
    start_time = time.time()
    result = agent.classify(doc_text)
    elapsed_ms = (time.time() - start_time) * 1000
    
    # Display results
    print("RESULT:")
    print(json.dumps(result, indent=2))
    print(f"\nTime: {elapsed_ms:.0f}ms")
    
    # Basic assertions
    print("\n" + "-" * 40)
    print("CHECKS:")
    
    # Check 1: Did it identify as invoice?
    is_invoice = result.get("document_type") == "invoice"
    print(f"  [{'✓' if is_invoice else '✗'}] Classified as invoice")
    
    # Check 2: Is confidence reasonable?
    confidence = result.get("confidence", 0)
    high_confidence = confidence >= 0.8
    print(f"  [{'✓' if high_confidence else '✗'}] Confidence >= 0.8 (got {confidence})")
    
    # Check 3: Did it extract vendor name?
    has_vendor = result.get("vendor_name") is not None
    print(f"  [{'✓' if has_vendor else '✗'}] Extracted vendor name: {result.get('vendor_name')}")
    
    # Check 4: Did it extract amount?
    has_amount = result.get("amount") is not None
    print(f"  [{'✓' if has_amount else '✗'}] Extracted amount: {result.get('amount')}")
    
    # Summary
    all_passed = is_invoice and high_confidence and has_vendor and has_amount
    print("\n" + "=" * 60)
    print(f"OVERALL: {'PASS ✓' if all_passed else 'FAIL ✗'}")
    print("=" * 60)
    
    return all_passed


def test_against_expected():
    """
    Compare router output against expected values.
    
    This is a simple version of what will become your evaluation framework.
    """
    
    print("\n" + "=" * 60)
    print("TEST: Compare Against Expected Output")
    print("=" * 60)
    
    # What we expect for the sample invoice
    expected = {
        "document_type": "invoice",
        "vendor_name": "Smith Concreting Pty Ltd",
        "project_name": "Balmoral Estate",
        "amount": 24200.00
    }
    
    # Get actual
    doc_text = load_sample_document("sample_invoice.txt")
    agent = RouterAgent()
    actual = agent.classify(doc_text)
    
    # Compare each field
    print("\nField-by-field comparison:")
    print("-" * 40)
    
    scores = []
    for field, expected_value in expected.items():
        actual_value = actual.get(field)
        
        # Simple matching logic (you'll make this smarter)
        if field == "amount":
            # Numeric tolerance
            try:
                match = abs(float(expected_value) - float(actual_value)) < 1.0
            except (TypeError, ValueError):
                match = False
        elif field in ["vendor_name", "project_name"]:
            # Case-insensitive contains
            match = (expected_value.lower() in str(actual_value).lower() or
                     str(actual_value).lower() in expected_value.lower())
        else:
            # Exact match
            match = expected_value == actual_value
        
        scores.append(1.0 if match else 0.0)
        status = "✓" if match else "✗"
        print(f"  [{status}] {field}")
        print(f"      Expected: {expected_value}")
        print(f"      Actual:   {actual_value}")
    
    accuracy = sum(scores) / len(scores) if scores else 0
    print("-" * 40)
    print(f"Accuracy: {accuracy:.0%} ({sum(scores):.0f}/{len(scores)} fields)")
    
    return accuracy >= 0.75  # Pass if 75%+ fields match


if __name__ == "__main__":
    print("\n🚀 Running Router Agent Tests\n")
    
    test1_passed = test_router_basic()
    test2_passed = test_against_expected()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Basic classification: {'PASS' if test1_passed else 'FAIL'}")
    print(f"  Expected comparison:  {'PASS' if test2_passed else 'FAIL'}")
    
    if test1_passed and test2_passed:
        print("\n✅ All tests passed! Ready to add more test cases.")
        print("\nNext steps:")
        print("  1. Add sample_progress_claim.txt and test it")
        print("  2. Add sample_contract.txt and test it")
        print("  3. Try with a real PDF from your files")
    else:
        print("\n❌ Some tests failed. Check the output above.")
