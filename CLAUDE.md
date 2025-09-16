# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is `trademe-sdk`, a Python SDK for the Trade Me API using OAuth 1.0a authentication. It's a proof-of-concept implementation with clean, layered architecture supporting multiple authentication methods and environments.

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

# Use command-line authentication utility
python -m trademe_sdk
```

## API Documentation

Use the included script to fetch consolidated OpenAPI specification for development context:

```bash
./src/scripts/get-consolidated-doc.sh
```

This copies documentation from `../trademe-api-doc/` to `./context/` for reference.

## Authentication Architecture

The SDK implements a layered authentication system with multiple credential sources:

### Authentication Flow Hierarchy (in order of preference):
1. **Saved credentials file** (`~/.config/trademe-sdk/credentials.json` or `%APPDATA%/trademe-sdk/credentials.json`)
2. **Environment variables** (all 4 required: `TM_CONSUMER_KEY`, `TM_CONSUMER_SECRET`, `TM_ACCESS_TOKEN`, `TM_ACCESS_SECRET`)
3. **Interactive OAuth flow** (if `auto_login=True` and running in terminal)

### Key Components:
- `ensure_auth()` - High-level credential resolution function
- `auth_flow.py` - OAuth 1.0a implementation with dual callback support (local server + PIN-based)
- `auth_helpers.py` - Convenience wrapper around auth flow
- `client.py` - HTTP client with OAuth 1.0a request signing

### Implementation Details:
- Uses PLAINTEXT signature method (simpler than HMAC-SHA1)
- Environment-based configuration (sandbox/production)
- Credentials automatically saved with secure permissions (0o600)

## Current Implementation

### Core Modules:
- `client.py` - TMClient class with OAuth 1.0a request signing
- `auth_flow.py` - OAuth 1.0a implementation with dual callback support
- `auth_helpers.py` - High-level ensure_auth() function
- `config.py` - Environment configuration (sandbox/production)
- `errors.py` - Custom exception classes

### API Client
- Environment-aware initialization (defaults to sandbox)
- Session-based HTTP handling with OAuth signing
- JSON response parsing with error handling
- Currently implements 2 proof-of-concept endpoints:
  - `get_listing(listing_id)` - Retrieve listing details
  - `get_watchlist(filter, page, rows, category)` - Retrieve user's watchlist

### Usage:
```python
auth = ensure_auth(auto_login=True, environment="sandbox")
client = TMClient(auth, environment="production")  # override environment
```