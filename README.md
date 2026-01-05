# Document Intelligence Starter

A minimal starting point for building a document processing agent with evaluation.

## What's in here

```
doc-intel-starter/
├── router_agent.py      # The one agent we're testing
├── test_router.py       # Simple test that runs the agent
├── sample_invoice.txt   # A fake invoice to test with
├── requirements.txt     # Dependencies
└── .env.example         # Copy to .env and add your API key
```

## Setup (5 minutes)

### Step 1: Clone and enter directory
```bash
git clone <your-repo-url>
cd doc-intel-starter
```

### Step 2: Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Add your API key
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### Step 5: Run the test
```bash
python test_router.py
```

You should see output showing the agent classifying the sample invoice.

## What to do next

Once this works, try these in order:

1. **Add a real document** - Replace sample_invoice.txt with an actual invoice PDF from your files
2. **Add more test cases** - Create sample_progress_claim.txt, sample_contract.txt
3. **Track accuracy** - Modify test_router.py to compare against expected outputs
4. **Add a second agent** - Create invoice_agent.py that extracts line items

## Milestone Checklist

- [ ] Router correctly classifies invoice
- [ ] Router correctly classifies progress claim  
- [ ] Router correctly classifies contract
- [ ] Added 5+ test documents
- [ ] Accuracy tracking working
- [ ] Invoice extraction agent built
- [ ] Validation agent built
- [ ] MCP server exposing metrics
