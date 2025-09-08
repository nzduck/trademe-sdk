from dataclasses import dataclass
from typing import Any, Dict, Optional
import requests
from requests_oauthlib import OAuth1
from oauthlib.oauth1 import SIGNATURE_PLAINTEXT
from .config import get_environment, DEFAULT_ENVIRONMENT

@dataclass
class TMAuth:
    consumer_key: str
    consumer_secret: str
    access_token: str
    access_token_secret: str

class TMClient:
    def __init__(self, auth: TMAuth, *, environment: str = DEFAULT_ENVIRONMENT, timeout: float = 20):
        env = get_environment(environment)
        self.base_url = env.api_base
        self.environment = environment
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "User-Agent": "trademe-sdk-poc/0.1",
        })
        self.session.auth = OAuth1(
            auth.consumer_key,
            client_secret=auth.consumer_secret,
            resource_owner_key=auth.access_token,
            resource_owner_secret=auth.access_token_secret,
            signature_method=SIGNATURE_PLAINTEXT
        )
        self.timeout = timeout

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        r = self.session.get(f"{self.base_url}{path}", params=params, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    # --- PoC endpoints ---
    def get_listing(self, listing_id: int) -> Dict[str, Any]:
        # GET /v1/listings/{listingId}.json
        return self._get(f"/v1/listings/{listing_id}.json")

    def get_watchlist(self, filter: str = "All", *, page: int = 1, rows: int = 50,
                      category: Optional[str] = None) -> Dict[str, Any]:
        # GET /v1/mytrademe/watchlist/{filter}.json
        params: Dict[str, Any] = {"page": page, "rows": rows}
        if category:
            params["category"] = category
        return self._get(f"/v1/mytrademe/watchlist/{filter}.json", params=params)
