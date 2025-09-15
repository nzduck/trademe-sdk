# Trade Me SDK

A Python SDK for the Trade Me API using OAuth 1.0a authentication. This proof-of-concept implementation provides a clean interface for Trade Me API operations with robust authentication handling and support for both sandbox and production environments.

## Installation

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
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

## Features

- **Multiple Authentication Methods**: Saved credentials, environment variables, or interactive OAuth flow
- **Environment Support**: Sandbox (default) and production environments
- **OAuth 1.0a Implementation**: Complete with dual callback support (local server + PIN-based)
- **Clean API**: Simple, intuitive interface with proper error handling
- **Session Management**: Persistent HTTP sessions with automatic request signing

## Authentication

The SDK supports multiple authentication methods in order of preference:

1. **Saved credentials file** (`~/.config/trademe-sdk/credentials.json` or `%APPDATA%/trademe-sdk/credentials.json`)
2. **Environment variables** (all 4 required: `TM_CONSUMER_KEY`, `TM_CONSUMER_SECRET`, `TM_ACCESS_TOKEN`, `TM_ACCESS_SECRET`)
3. **Interactive OAuth flow** (when `auto_login=True` and running in terminal)

### Command-line Authentication

```bash
# Interactive OAuth setup
python -m trademe_sdk
```

## API Operations

Current SDK operations (proof-of-concept):

- **`get_listing(listing_id)`** - Retrieve listing details
- **`get_watchlist(filter, page, rows, category)`** - Retrieve user's watchlist with pagination

### Usage Examples

```python
# Get a specific listing
listing = client.get_listing(2149713189)
print(f"Title: {listing.get('Title')}")

# Get watchlist with filters
watchlist = client.get_watchlist(
    filter="All",
    page=1,
    rows=10,
    category="Electronics"  # Optional category filter
)
print(f"Total items: {watchlist.get('TotalCount')}")
```

## Examples

See `src/examples/` for complete usage examples:
- **`demo.py`** - Basic SDK usage with authentication and API calls
- **`login_demo.py`** - OAuth authentication flow demonstration

## Environments

The SDK supports both Trade Me environments:

- **`sandbox`** (default) - Trade Me sandbox for testing
- **`production`** - Live Trade Me environment

```python
# Explicitly specify environment
auth = ensure_auth(auto_login=True, environment="production")
client = TMClient(auth, environment="production")
```

## Extending the SDK

When developing or extending this proof-of-concept SDK, it can be helpful to provide clean documentation on Trade Me's API structure to LLM agents for context. Comprehensive API documentation is available at:

**https://github.com/nzduck/trademe-api-doc**

This repository contains:
- Complete OpenAPI specifications for Trade Me's API
- Consolidated documentation in machine-readable formats
- Detailed endpoint descriptions and schemas

For convenience, use the included script to fetch consolidated documentation:

```bash
# Fetch API documentation for development context
./src/scripts/get-consolidated-doc.sh
```

This copies the consolidated OpenAPI specification to `./context/` for easy reference when implementing new endpoints.

## Project Structure

```
src/
├── trademe_sdk/
│   ├── __init__.py          # Main exports
│   ├── __main__.py          # Command-line interface
│   ├── client.py            # TMClient and TMAuth classes
│   ├── auth_flow.py         # OAuth 1.0a implementation
│   ├── auth_helpers.py      # High-level auth functions
│   ├── config.py            # Environment configuration
│   └── errors.py            # Custom exceptions
├── examples/
│   ├── demo.py              # Basic usage example
│   └── login_demo.py        # OAuth flow example
└── scripts/
    └── get-consolidated-doc.sh  # API documentation fetcher
```