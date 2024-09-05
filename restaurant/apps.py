"""
Restaurant apps module
"""
from django.apps import AppConfig

# Restaurant configuration object
class RestaurantConfig(AppConfig):
    """Reservation configurations.
    Attributes:
        default_auto_field
        name
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'restaurant'
