import logging
import json
import time
from django.utils.deprecation import MiddlewareMixin

# Logger for API requests/responses
logger = logging.getLogger('api_logger')

class APILoggingMiddleware(MiddlewareMixin):
    """
    Logs all incoming requests and responses with server time and processing time.
    """
    def process_request(self, request):
        request.start_time = time.time()
        try:
            body = request.body.decode('utf-8')
            if body:
                data = json.loads(body)
            else:
                data = {}
        except Exception:
            data = str(request.body)

        logger.info(
            f"Request | User: {getattr(request.user, 'username', 'Anonymous')} "
            f"| Path: {request.path} | Method: {request.method} | Data: {data}"
        )

    def process_response(self, request, response):
        try:
            content = response.content.decode('utf-8')
        except Exception:
            content = str(response.content)

        duration = round(time.time() - request.start_time, 3) if hasattr(request, 'start_time') else None

        logger.info(
            f"Response | User: {getattr(request.user, 'username', 'Anonymous')} "
            f"| Path: {request.path} | Status: {response.status_code} | "
            f"Duration: {duration}s | Data: {content}"
        )
        return response
