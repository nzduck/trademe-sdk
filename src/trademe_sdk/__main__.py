from .auth_flow import login
from .config import DEFAULT_ENVIRONMENT

def main():
    ck = input("Consumer key: ").strip()
    cs = input("Consumer secret: ").strip()
    env = input(f"Environment (default: {DEFAULT_ENVIRONMENT}): ").strip() or DEFAULT_ENVIRONMENT
    login(ck, cs, prefer_local_callback=False, environment=env)

if __name__ == "__main__":
    main()
