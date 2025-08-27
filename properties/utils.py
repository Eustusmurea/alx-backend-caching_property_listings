from django.core.cache import cache
from .models import Property
import logging
from django_redis import get_redis_connection

logger = logging.getLogger(__name__)

def get_all_properties():
    """
    Retrieves all properties, caching the queryset in Redis for 1 hour.
    """
    properties = cache.get('all_properties')
    if properties is None:
        properties = list(Property.objects.all())  # cast to list (querysets aren't directly cacheable)
        cache.set('all_properties', properties, 3600)  # 1 hour
    return properties

def get_redis_cache_metrics():
    """
    Retrieve Redis cache hit/miss metrics and calculate hit ratio.
    """
    try:
        # connect to redis
        conn = get_redis_connection("default")

        # fetch stats
        info = conn.info("stats")
        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)

        # calculate ratio
        total = hits + misses
        hit_ratio = (hits / total) if total > 0 else 0.0

        metrics = {
            "keyspace_hits": hits,
            "keyspace_misses": misses,
            "hit_ratio": round(hit_ratio, 2),
        }

        logger.info(f"Redis Cache Metrics: {metrics}")
        return metrics

    except Exception as e:
        logger.error(f"Error retrieving Redis cache metrics: {e}")
        return {
            "keyspace_hits": 0,
            "keyspace_misses": 0,
            "hit_ratio": 0.0,
        }
