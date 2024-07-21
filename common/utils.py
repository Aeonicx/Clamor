from rest_framework.response import Response as RestResponse


# default success Response
class Response(RestResponse):
    def __init__(self, success=True, status=None, message=None, data=None, **kwargs):
        response_data = {
            "success": success,
            "status": status,
            "message": message or "Success",
        }
        response_data.update(**kwargs)
        response_data.update({"data": data})
        response_data = {
            key: value for key, value in response_data.items() if value is not None
        }

        super().__init__(data=response_data, status=status)
