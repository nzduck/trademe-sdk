# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This appears to be a new/empty project directory named `trademe-sdk`. The repository is currently empty with no existing files, package.json, or configuration files.

## Development Setup

Since this is an empty project, the development workflow will depend on what type of SDK is being built. Common patterns for SDK development include:

- For Node.js SDKs: Initialize with `npm init` and add TypeScript configuration
- For REST API SDKs: Typically include HTTP client, authentication, and API endpoint modules
- For TradeMe specifically: Likely needs OAuth authentication and marketplace API integration

## Architecture Considerations

When implementing this TradeMe SDK, consider:

- Authentication layer (OAuth 1.0a or OAuth 2.0 depending on TradeMe's API)
- API client with rate limiting and error handling
- Type definitions for TradeMe API responses
- Modular structure separating different API domains (listings, bidding, user management, etc.)

## Next Steps

This project needs initial setup. Consider:
1. Adding package.json with appropriate dependencies
2. Setting up TypeScript configuration
3. Implementing core SDK structure
4. Adding authentication mechanisms
5. Creating API client foundations