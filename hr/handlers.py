"""booking-sys handlers module for Mapping & Logic for 4xx to 5xx HTTP status codes
"""
import logging
from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest
from django.urls.exceptions import Resolver404
from django.http import HttpResponse

logger = logging.getLogger(__name__)

class Handlers():
    """Handlers for HTTP Error codes like 404 not found, 401 forbidden etc.
    """

    @classmethod
    def handler404(cls, request:WSGIRequest, exception:Resolver404) -> HttpResponse:
        """Resolve bad request path
        Parameters
        ----------
        request : WSGIRequest
        exception: Resolver404
        """
        uri = request.get_full_path
        logger.error('Bad Request URI path: %s', uri)
        return render(request, 'error.html', {'uri': uri}, status=404)
