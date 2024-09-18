"""booking-sys Handlers Mapping & Logic for 4xx to 5xx HTTP status codes
"""
from django.shortcuts import render
import logging

logger = logging.getLogger(__name__)

class Handlers(object):

    @classmethod
    def handler404(cls, request, exception):
        """Resolve bad request path
        Parameters
        ----------
        request : Requests https://requests.readthedocs.io/en/latest/
        """
        uri = request.get_full_path
        logger.error('Bad Request URI path: %s', uri)
        return render(request, 'error.html', {'uri': uri}, status=404)