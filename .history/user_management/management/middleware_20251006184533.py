import logging
import json
import time
from datetime import datetime, timezone, timedelta
from django.utils.deprecation import MiddlewareMixin


# Logger for API requests/responses
logger = logging.getLogger('api_logger')

IST = timezone(timedelta(hours=5, minutes=30))  # IST timezone

class APILoggingMiddleware(MiddlewareMixin):
    """
    Logs all incoming requests and responses with server time, IST, and processing time.
    """
    def process_request(self, request):
        request.start_time = time.time()
        try:
            body = request.body.decode('utf-8')
            data = json.loads(body) if body else {}
        except Exception:
            data = str(request.body)

        server_time = datetime.now()
        ist_time = datetime.now(IST)

        logger.info(
            f"Request | User: {getattr(request.user, 'username', 'Anonymous')} "
            f"| Path: {request.path} | Method: {request.method} | Data: {data} "
            f"| ServerTime: {server_time} | ISTTime: {ist_time}"
        )

    def process_response(self, request, response):
    # Determine response type
    content_type = response.get('Content-Type', '')

    # If JSON, try to decode, otherwise just log a short summary
    if 'application/json' in content_type:
        try:
            content = json.loads(response.content.decode('utf-8'))
        except Exception:
            content = str(response.content)
    elif 'text/html' in content_type:
        content = f"<HTML content, length={len(response.content)}>"
    else:
        try:
            content = response.content.decode('utf-8')
        except Exception:
            content = str(response.content)

    duration = round(time.time() - request.start_time, 3) if hasattr(request, 'start_time') else None
    server_time = datetime.now()
    ist_time = datetime.now(IST)

    logger.info(
        f"Response | User: {getattr(request.user, 'username', 'Anonymous')} "
        f"| Path: {request.path} | Status: {response.status_code} | Duration: {duration}s "
        f"| ServerTime: {server_time} | ISTTime: {ist_time} | Data: {content}"
    )
    return response

