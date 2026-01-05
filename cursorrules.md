# Document Intelligence Project - Cursor Rules

## Project Overview

This is a multi-agent document processing system for Song Capital Group, an Australian property development company. The system classifies and extracts data from construction/development documents (invoices, progress claims, contracts, variations, settlement statements).

**Current stage:** Early development - building and testing one agent at a time.

**End goal:** A testable, production-ready pipeline with:
- Router agent (classifies documents)
- Specialist extraction agents (invoice, progress claim, contract, etc.)
- Validation agent (cross-references against budgets/contracts)
- MCP server exposing metrics to Claude
- Evaluation framework tracking accuracy over time

## Tech Stack

- **Language:** Python 3.11+
- **LLM:** Anthropic Claude (claude-sonnet-4-20250514)
- **Key libraries:** anthropic, python-dotenv, pytest (later), pydantic (later)
- **Testing:** Start simple with assert statements, migrate to pytest
- **Environment:** Virtual environment (venv), API key in .env file

## Code Style

### General Principles
- Keep files short and focused (under 200 lines ideally)
- One agent per file
- Prefer simple dict returns initially, migrate to Pydantic models later
- Always include docstrings explaining what the function does
- Use type hints

### Agent Pattern
All agents should follow this structure:

```python
class SomeAgent:
    def __init__(self):
        self.client = Anthropic()
        self.model = "claude-sonnet-4-20250514"
        self.prompt_version = "v1"  # Track for evaluation
    
    def process(self, input_data: str) -> dict:
        """One clear method that does the main work."""
        # 1. Build prompt
        # 2. Call Claude
        # 3. Parse response
        # 4. Return structured dict
        pass
```

### Prompt Engineering
- System prompts should be clear and specific
- Always request JSON output with explicit schema
- Include confidence scoring guidelines
- List known document types/vendors/projects to help classification

### Error Handling
- Wrap JSON parsing in try/except
- Return sensible defaults on failure
- Include error info in response for debugging

## File Structure

```
doc-intel-starter/
├── router_agent.py        # Document classifier
├── invoice_agent.py       # Invoice data extraction (TODO)
├── progress_claim_agent.py # Progress claim extraction (TODO)
├── validation_agent.py    # Cross-reference validation (TODO)
├── orchestrator.py        # Chains agents together (TODO)
├── test_router.py         # Tests for router
├── test_invoice.py        # Tests for invoice agent (TODO)
├── evaluation/            # Evaluation framework (TODO)
│   ├── metrics.py
│   └── golden_dataset/
├── mcp_server/            # MCP server (TODO)
│   └── server.py
├── sample_invoice.txt     # Test documents
├── sample_progress_claim.txt
└── sample_contract.txt
```

## Domain Knowledge

### Document Types
1. **Invoice** - Bill for goods/services, has ABN, GST, line items
2. **Progress Claim** - Contractor claiming payment for completed work stages
3. **Contract** - Formal agreement, has parties, terms, schedules
4. **Variation** - Change to existing contract, references original
5. **Settlement** - Property settlement statement, final amounts

### Key Fields to Extract
- Vendor name and ABN
- Project reference (e.g., "Balmoral Estate", "Alfred Road")
- Amounts (subtotal, GST, total)
- Dates (invoice date, due date)
- References (PO numbers, contract numbers)
- Line items with categories

### Categories for Line Items
- construction (building work, trades)
- professional_fees (architects, engineers, lawyers)
- materials (concrete, timber, fixtures)
- equipment_hire (machinery, tools)
- council_fees (permits, inspections)
- utilities (water, power connections)

## Testing Approach

### Current (Simple)
```python
# Load document
doc = load_sample_document("sample_invoice.txt")

# Run agent
result = agent.classify(doc)

# Check key fields
assert result["document_type"] == "invoice"
assert result["confidence"] >= 0.8
```

### Future (With Evaluation)
```python
# Golden dataset with expected outputs
expected = load_expected("invoice_001.json")
actual = agent.classify(doc)

# Field-by-field comparison
score = evaluate(expected, actual, rules={
    "vendor_name": "fuzzy_match_0.8",
    "amount": "numeric_tolerance_1.0"
})
```

## Common Tasks

### Adding a New Agent
1. Create `{name}_agent.py` following the agent pattern
2. Create `sample_{name}.txt` with a test document
3. Create `test_{name}.py` with basic tests
4. Run tests to verify

### Adding a Test Document
1. Save document text to `sample_{type}.txt`
2. Anonymize sensitive info (use fake names/ABNs)
3. Add expected output to test file
4. Run tests

### Improving Accuracy
1. Check which fields are failing in tests
2. Update the system prompt in the agent
3. Increment `prompt_version` (e.g., "v1" → "v2")
4. Re-run tests and compare

### Debugging Classification Issues
1. Print the raw Claude response
2. Check if JSON parsing failed
3. Look at the "reasoning" field
4. Try adding examples to the prompt

## Important Reminders

- **API Key:** Never commit .env file. Use .env.example as template.
- **Costs:** Claude Sonnet is ~$3/1M input tokens. A test run costs ~$0.01.
- **Rate Limits:** If tests fail with rate limit errors, add small delays.
- **JSON Output:** Always tell Claude to respond with JSON only, no markdown.

## Current TODO

1. [ ] Test router with real documents from Song Capital
2. [ ] Add progress claim sample and test
3. [ ] Add contract sample and test
4. [ ] Build invoice extraction agent
5. [ ] Add accuracy tracking to tests
6. [ ] Build validation agent
7. [ ] Build MCP server

## Questions to Ask Cursor

Good prompts for this project:
- "Add a new agent for extracting progress claim data"
- "Update test_router.py to track accuracy across multiple documents"
- "Add Pydantic models for the invoice extraction output"
- "Create a simple orchestrator that chains router → invoice agent"
- "Add pytest fixtures for loading test documents"
