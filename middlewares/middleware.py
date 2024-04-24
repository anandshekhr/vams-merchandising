# middleware.py

from django.utils.deprecation import MiddlewareMixin
from .models import RequestDataLog  # Import your model for storing request data
from ua_parser import user_agent_parser

class RequestDataMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Extract relevant data from the request
        method = request.method
        path = request.path
        body = request.body
        user_agent_string = request.META.get('HTTP_USER_AGENT', '')

        # Parse the user agent string to determine if it's a mobile device
        parsed_user_agent = user_agent_parser.Parse(user_agent_string)
        device_family = parsed_user_agent['device']['family']

        # Check if the device family corresponds to a mobile device
        is_mobile = True if device_family in ['iPhone', 'iPad', 'Android', 'Windows Phone', 'BlackBerry', 'Mobile'] else False

        
        # Save the request data to your database
        RequestDataLog.objects.create(
            method=method,
            path=path,
            body=body,
            user_agent=user_agent_string,
            mobile=is_mobile
        )
