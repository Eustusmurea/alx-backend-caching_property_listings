from django.core.cache import cache
from .models import Property
import logging

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
    Connects to Redis via django_redis, retrieves cache hit/miss metrics,
    calculates hit ratio, logs metrics, and returns them.
    """
    try:
        client = cache.client.get_client()
        info = client.info()

        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)
        total_requests = hits + misses

        # required one-liner with inline conditional
        hit_ratio = hits / total_requests if total_requests > 0 else 0

        metrics = {
            "hits": hits,
            "misses": misses,
            "hit_ratio": hit_ratio,
        }

        logger.info(f"Redis cache metrics: {metrics}")
        return metrics

    except Exception as e:
        logger.error(f"Error retrieving Redis cache metrics: {e}")
        return {"hits": 0, "misses": 0, "hit_ratio": 0}
