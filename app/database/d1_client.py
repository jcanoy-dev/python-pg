from cloudflare import Cloudflare
from app.core.config import settings

# Thread-safe database SDK engine instantiation
cf_d1_engine = Cloudflare(api_token=settings.CLOUDFLARE_API_TOKEN)

def get_d1_client() -> Cloudflare:
    """Enterprise Dependency injection hook.
    Allows easy mocking of the database connection layer during automated testing."""
    return cf_d1_engine
