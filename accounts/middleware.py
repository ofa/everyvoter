"""NewRelice Account-Related Middleware"""
import newrelic.agent


class NewRelicUserMiddleware(object):
    """Middleware to add the current user to NewRelic"""

    def __init__(self, get_response):
        """Initialize the Middleware"""
        self.get_response = get_response


    def __call__(self, request):
        """Process a request"""

        if hasattr(request, 'user'):
            newrelic.agent.add_custom_parameter('user_id', request.user.id)

        return self.get_response(request)
