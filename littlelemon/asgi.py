"""
ASGI config for littlelemon project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""
from django.core.asgi import get_asgi_application # type: ignore
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "littlelemon.settings")

application = get_asgi_application()
