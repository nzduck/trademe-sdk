from typing import Dict, NamedTuple

class Environment(NamedTuple):
    """Configuration for a Trade Me API environment."""
    api_base: str
    oauth_base: str
    
    @property
    def request_token_url(self) -> str:
        return f"{self.api_base}/Oauth/RequestToken"
    
    @property
    def access_token_url(self) -> str:
        return f"{self.api_base}/Oauth/AccessToken"
    
    @property
    def authorize_url(self) -> str:
        return f"{self.oauth_base}/Oauth/Authorize"

# Environment configurations
ENVIRONMENTS: Dict[str, Environment] = {
    "sandbox": Environment(
        api_base="https://api.tmsandbox.co.nz",
        oauth_base="https://www.tmsandbox.co.nz"
    ),
    "production": Environment(
        api_base="https://api.trademe.co.nz", 
        oauth_base="https://www.trademe.co.nz"
    ),
}

DEFAULT_ENVIRONMENT = "sandbox"

def get_environment(name: str = DEFAULT_ENVIRONMENT) -> Environment:
    """Get environment configuration by name."""
    if name not in ENVIRONMENTS:
        available = ", ".join(ENVIRONMENTS.keys())
        raise ValueError(f"Unknown environment '{name}'. Available: {available}")
    return ENVIRONMENTS[name]