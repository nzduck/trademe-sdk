import os, sys
from .errors import AuthenticationRequired
from .auth_flow import login, load_credentials
from .client import TMAuth
from .config import DEFAULT_ENVIRONMENT

def ensure_auth(*, consumer_key: str | None = None,
                consumer_secret: str | None = None,
                auto_login: bool = False,
                environment: str = DEFAULT_ENVIRONMENT) -> TMAuth:
    """
    Resolve credentials for Trade Me API access.

    Order:
    1) Saved credentials file
    2) All 4 env vars (TM_CONSUMER_KEY, TM_CONSUMER_SECRET, TM_ACCESS_TOKEN, TM_ACCESS_SECRET)
    3) If auto_login=True and interactive, run OAuth login() with PIN flow

    Otherwise raises AuthenticationRequired.
    """
    creds = load_credentials()
    if creds:
        return TMAuth(creds.consumer_key, creds.consumer_secret,
                      creds.access_token, creds.access_token_secret)

    ck = consumer_key or os.getenv("TM_CONSUMER_KEY")
    cs = consumer_secret or os.getenv("TM_CONSUMER_SECRET")
    at, asec = os.getenv("TM_ACCESS_TOKEN"), os.getenv("TM_ACCESS_SECRET")

    if ck and cs and at and asec:
        return TMAuth(ck, cs, at, asec)

    if auto_login and sys.stdin.isatty():
        if not ck or not cs:
            ck = input("Consumer key: ").strip()
            cs = input("Consumer secret: ").strip()
        creds = login(ck, cs, prefer_local_callback=False, environment=environment)
        return TMAuth(creds.consumer_key, creds.consumer_secret,
                      creds.access_token, creds.access_token_secret)

    raise AuthenticationRequired(
        "No credentials found. Run `python -m trademe_sdk.login` or call login() interactively."
    )
