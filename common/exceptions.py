from rest_framework.views import exception_handler


# custom error message showing
def custom_rest_framework_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None:
        # Retrieve the actual status code from the response
        status_code = response.status_code

        # Customize the error messages here
        if isinstance(response.data, list):
            new_data = {
                "success": False,
                "status": status_code,
                "errors": {"non_field_errors": [e for e in response.data]},
            }
            response.data = new_data

        elif isinstance(response.data, dict):
            new_data = {
                "success": False,
                "status": status_code,
                "errors": {k: v for k, v in response.data.items()},
            }
            response.data = new_data

    return response
