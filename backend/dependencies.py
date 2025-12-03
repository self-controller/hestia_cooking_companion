import redis
from config import REDIS_URL

# Global Redis client instance
redis_client: redis.Redis | None = None

def get_redis() -> redis.Redis:
    """
    Dependency function to get Redis client.
    Note: redis_client must be initialized before use (typically in lifespan).
    """
    assert redis_client is not None, "Redis not initialized"
    return redis_client

def set_redis_client(client: redis.Redis | None) -> None:
    """
    Set the global Redis client. Used by lifespan in main.py.
    """
    global redis_client
    redis_client = client