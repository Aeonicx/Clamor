from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse


class ExceptionMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed before the view is called
        response = self.get_response(request)
        # Code to be executed after the view is called
        return response

    def process_exception(self, request, exception):
        # handle all exceptions
        response = {
            "success": False,
            "status": 500,
            "errors": {
                "non_field_errors": "Something went wrong.",
                "sys_msg": str(exception),
            },
        }

        return JsonResponse(response, status=500)
