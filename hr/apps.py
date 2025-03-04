"""
HR apps module
"""
from django.apps import AppConfig

# HR configuration object
class HrConfig(AppConfig):
    """Reservation configurations.
    Attributes:
        default_auto_field
        name
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hr'
