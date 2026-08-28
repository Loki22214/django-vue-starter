from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckView(APIView):
    """
    Health check endpoint to verify that the application is running.
    """

    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"status": "healthy"})
