from rest_framework.response import Response
from rest_framework import status

def validate_request_data(fn):
    def decorated(*args, **kwargs):
        name = args[0].request.data.get("name", "")
        description = args[0].request.data.get("description", "")
        price = args[0].request.data.get("price", "")

        if not name or not description or not price:
            return Response(
                data={
                    "message": "All fields are required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return fn(*args, **kwargs)
    return decorated
