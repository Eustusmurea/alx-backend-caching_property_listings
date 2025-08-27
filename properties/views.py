from django.http import JsonResponse
from .utils import get_all_properties

def property_list(request):
    """
    Returns all properties, using Redis cache for queryset.
    """
    properties = get_all_properties()
    data = [{"id": prop.id, "title": prop.title, "price": prop.price} for prop in properties]
    return JsonResponse(data, safe=False)
