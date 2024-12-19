https://highsixoauth2.pythonanywhere.com/

# OAuth2 Authlib

A demonstration of an OAuth 2.0 Client-Server implementation using **Authlib** and Flask.

## Features

### Server

- Implements a fully functional OAuth 2.0 server with support for all standard grant types.
- Built with Flask and **Authlib**, providing easy customization and extension.
- Uses SQLite as the database for storing credentials and token data.

### Client

- Implements an OAuth 2.0 client capable of interacting with the custom OAuth 2.0 server.
- Supports integration with third-party OAuth 2.0 providers, such as:
  - Discord
  - X (formerly Twitter)
  - Google
- Includes PKCE (Proof Key for Code Exchange) for enhanced security during the authorization flow.
- All integrations are based on the `Authorization Code Grant`.

## Requirements

- Python 3.7 or higher
- Flask
- Authlib
- SQLite

## Getting Started

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Setting up the Server

1. Navigate to the `oauth2-server` directory:

   ```bash
   cd oauth2-server
   ```

2. Run the server:

   ```bash
   flask run
   ```

### Setting up the Client

1. Navigate to the `oauth2-client` directory:

   ```bash
   cd oauth2-client
   ```

2. Configure the `.env` file with the appropriate credentials for your OAuth 2.0 server and third-party providers.

3. Run the client:

   ```bash
   flask run
   ```

## Project Structure

### oauth2-server

- **app.py**: Entry point for running the OAuth 2.0 server.
- **website/**: Contains the core logic for the OAuth server, including token generation and validation.
- **instance/**: Stores the SQLite database.

### oauth2-client

- **app.py**: Entry point for running the OAuth 2.0 client.
- **config.py**: Configuration for client credentials and third-party integrations.
- **templates/**: HTML templates for the client interface.
- **static/**: Static assets (CSS, JavaScript) for the client.
