from __future__ import annotations
import json, os, threading, webbrowser
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Optional
from requests_oauthlib import OAuth1Session
from oauthlib.oauth1 import SIGNATURE_PLAINTEXT
from .config import get_environment, DEFAULT_ENVIRONMENT

def _default_cred_path() -> Path:
    if os.name == "nt":
        base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
    else:
        base = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    return Path(os.environ.get("TM_CRED_FILE", str(base / "trademe-sdk" / "credentials.json")))

CRED_PATH = _default_cred_path()

@dataclass
class Credentials:
    consumer_key: str
    consumer_secret: str
    access_token: str
    access_token_secret: str

def save_credentials(creds: Credentials) -> None:
    CRED_PATH.parent.mkdir(parents=True, exist_ok=True)
    CRED_PATH.write_text(json.dumps({
        "consumer_key": creds.consumer_key,
        "consumer_secret": creds.consumer_secret,
        "access_token": creds.access_token,
        "access_token_secret": creds.access_token_secret,
    }, indent=2))
    try:
        os.chmod(CRED_PATH, 0o600)  # best-effort
    except Exception:
        pass

def load_credentials() -> Optional[Credentials]:
    if not CRED_PATH.exists():
        return None
    data = json.loads(CRED_PATH.read_text())
    return Credentials(
        consumer_key=data["consumer_key"],
        consumer_secret=data["consumer_secret"],
        access_token=data["access_token"],
        access_token_secret=data["access_token_secret"],
    )

# ---- local callback server (loopback) ----
class _CallbackHandler(BaseHTTPRequestHandler):
    verifier: Optional[str] = None
    done = threading.Event()

    def do_GET(self):
        from urllib.parse import urlparse, parse_qs
        qs = parse_qs(urlparse(self.path).query)
        _CallbackHandler.verifier = (qs.get("oauth_verifier") or [""])[0]
        self.send_response(200); self.end_headers()
        self.wfile.write(b"You may close this tab and return to the terminal.")
        _CallbackHandler.done.set()

    def log_message(self, format, *args):  # silence logs
        pass

def _capture_verifier_via_local_callback(port=8765, timeout=180) -> Optional[str]:
    _CallbackHandler.verifier = None
    _CallbackHandler.done.clear()
    server = HTTPServer(("127.0.0.1", port), _CallbackHandler)
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    try:
        _CallbackHandler.done.wait(timeout=timeout)
    finally:
        server.shutdown()
        server.server_close()
        t.join(timeout=1)
    return _CallbackHandler.verifier

# ---- main login flow ----
def login(consumer_key: str,
          consumer_secret: str,
          *,
          scope: str = "MyTradeMeRead,MyTradeMeWrite",
          prefer_local_callback: bool = True,
          environment: str = DEFAULT_ENVIRONMENT) -> Credentials:
    """
    Guides the user through OAuth 1.0a and returns/saves access token + secret.
    If prefer_local_callback=True, uses http://127.0.0.1:8765/callback.
    Otherwise uses 'oob' PIN flow.
    """
    env = get_environment(environment)
    callback_uri = "http://127.0.0.1:8765/callback" if prefer_local_callback else "oob"

    # 1) Request token (use PLAINTEXT for simplicity)
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        callback_uri=callback_uri,
        signature_method=SIGNATURE_PLAINTEXT,
    )
    rt = oauth.fetch_request_token(env.request_token_url, data={'scope': scope})

    # 2) Open authorize URL in the browser
    auth_url = oauth.authorization_url(env.authorize_url)
    print("Opening browser for authorization...")
    webbrowser.open(auth_url)

    # 3) Capture verifier
    if callback_uri == "oob":
        verifier = input("Enter the PIN / oauth_verifier from the browser: ").strip()
    else:
        print("Waiting for authorization (capturing callback on 127.0.0.1:8765)...")
        verifier = _capture_verifier_via_local_callback() or input("Paste the oauth_verifier: ").strip()

    # 4) Exchange for access token
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=rt["oauth_token"],
        resource_owner_secret=rt["oauth_token_secret"],
        verifier=verifier,
        signature_method=SIGNATURE_PLAINTEXT,
    )
    at = oauth.fetch_access_token(env.access_token_url)

    creds = Credentials(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=at["oauth_token"],
        access_token_secret=at["oauth_token_secret"],
    )
    save_credentials(creds)
    print(f"Saved credentials to: {CRED_PATH}")
    return creds
