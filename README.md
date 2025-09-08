# Trade Me SDK

A Python SDK for the Trade Me API using OAuth 1.0a authentication.

## Installation

```bash
pip install -e .
```

## Quick Start

```python
from trademe_sdk import TMClient, ensure_auth

# Authenticate (interactive OAuth flow)
auth = ensure_auth(auto_login=True)

# Create client (defaults to sandbox)
client = TMClient(auth)

# Use the API
listing = client.get_listing(2149713189)
watchlist = client.get_watchlist("All", page=1, rows=10)
```

## Authentication

The SDK supports multiple authentication methods:
1. Saved credentials file (`~/.config/trademe-sdk/credentials.json`)
2. Environment variables (`TM_CONSUMER_KEY`, `TM_CONSUMER_SECRET`, `TM_ACCESS_TOKEN`, `TM_ACCESS_SECRET`)
3. Interactive OAuth flow

## Operations

Current SDK operations:

- **`get_listing(listing_id)`** - Retrieve listing details
- **`get_watchlist(filter, page, rows, category)`** - Retrieve user's watchlist

## Examples

See `src/examples/` for complete usage examples:
- `demo.py` - Basic SDK usage
- `login_demo.py` - OAuth authentication flow

## Environments

- **sandbox** (default) - Trade Me sandbox for testing
- **production** - Live Trade Me environment