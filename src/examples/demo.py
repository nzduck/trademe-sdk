import os
from dotenv import load_dotenv
from trademe_sdk import TMClient
from trademe_sdk import ensure_auth

load_dotenv()

auth = ensure_auth(
    consumer_key=os.getenv("TM_CONSUMER_KEY"),
    consumer_secret=os.getenv("TM_CONSUMER_SECRET"),
    auto_login=True,   # demo is interactive, so auto-login is allowed
    environment="sandbox"  # explicitly specify sandbox (this is also the default)
)
client = TMClient(auth)  # no need to specify URL anymore!

# 1) Listing details
listing_id = 2149713189  # this is a current sandbox ID
try:
    listing = client.get_listing(listing_id)
    print("Listing title:", listing.get("Title"))
except Exception as e:
    print("Listing call failed:", e)

# 2) Watchlist
try:
    wl = client.get_watchlist("All", page=1, rows=10)
    items = wl.get("List") or wl.get("Items") or []
    print("Watchlist total:", wl.get("TotalCount", len(items)))
    print("Returned items:", len(items))
except Exception as e:
    print("Watchlist call failed:", e)
