from trademe_sdk import login, load_credentials, DEFAULT_ENVIRONMENT

# Prompt for consumer key/secret (or set TM_CONSUMER_KEY / TM_CONSUMER_SECRET in .env first)
ck = input("Consumer key: ").strip()
cs = input("Consumer secret: ").strip()
env = input(f"Environment (default: {DEFAULT_ENVIRONMENT}): ").strip() or DEFAULT_ENVIRONMENT

creds = login(ck, cs, prefer_local_callback=False, environment=env)  # use PIN/OOB fallback
print("Got tokens!")
print("Access token:", creds.access_token)
print("Access secret:", creds.access_token_secret)
