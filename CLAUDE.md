# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is `trademe-sdk`, a Python SDK for the Trade Me API using OAuth 1.0a authentication. It's currently a proof-of-concept implementation with basic functionality for listing details and watchlist operations.

## Development Commands

```bash
# Install in development mode (create virtual environment first)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .

# Get Trade Me API documentation for context
./src/scripts/get-consolidated-doc.sh

# Run examples
python src/examples/demo.py               # Main demo (sandbox environment)
python src/examples/login_demo.py         # OAuth login demo (PIN-based OOB flow)

# Use command-line login utility
python -m trademe_sdk
```

## API Documentation

To fetch the consolidated OpenAPI specification for development context:

```bash
./src/scripts/get-consolidated-doc.sh
```

This copies `../trademe-api-doc/openapi/openapi-consolidated.yaml` to `./context/` for reference when implementing new endpoints.

## Authentication Architecture

The SDK implements a layered authentication system with multiple credential sources:

### Authentication Flow Hierarchy (in order of preference):
1. **Saved credentials file** (`~/.config/trademe-sdk/credentials.json` or `%APPDATA%/trademe-sdk/credentials.json`)
2. **Environment variables** (all 4 required: `TM_CONSUMER_KEY`, `TM_CONSUMER_SECRET`, `TM_ACCESS_TOKEN`, `TM_ACCESS_SECRET`)
3. **Interactive OAuth flow** (if `auto_login=True` and running in terminal)

### Key Components:
- `ensure_auth()` - High-level credential resolution function used by demo.py
- `auth_flow.py` - Low-level OAuth 1.0a implementation with dual callback support:
  - **Local callback server** (`prefer_local_callback=True`) - Opens browser, captures redirect automatically
  - **PIN-based OOB flow** (`prefer_local_callback=False`) - User manually enters PIN from browser
- `auth_helpers.py` - Convenience wrapper around auth flow
- `client.py` - HTTP client with OAuth 1.0a request signing

### OAuth Implementation Details:
- Uses **PLAINTEXT signature method** throughout (simpler than HMAC-SHA1)
- **Environment-based configuration** - no need to specify URLs manually
- Scope parameter sent as POST data to request token endpoint (not query string)
- Local callback server runs on `127.0.0.1:8765` with proper cleanup
- Credentials automatically saved to secure file with 0o600 permissions

## Environment Configuration

The SDK supports multiple Trade Me environments via the `environment` parameter:

- **"sandbox"** (default) - Trade Me sandbox for testing
- **"production"** - Live Trade Me environment

All URLs (API base, OAuth endpoints) are automatically configured based on environment selection.

## API Client Structure

The `TMClient` class provides:
- **Environment-aware initialization** - defaults to sandbox, can specify production
- Session-based HTTP handling with OAuth 1.0a signing
- JSON response parsing with error handling
- Currently implements 2 endpoints as proof-of-concept:
  - `get_listing(listing_id)` - Retrieve listing details
  - `get_watchlist(filter, page, rows, category)` - Retrieve user's watchlist

### Usage Examples:

```python
# Sandbox (default)
client = TMClient(auth)

# Production
client = TMClient(auth, environment="production")

# Environment can also be specified during auth
auth = ensure_auth(auto_login=True, environment="production")
```

## Error Handling

- `AuthenticationRequired` exception raised when no valid credentials found
- HTTP errors bubble up from requests library with `raise_for_status()`