from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import MLRequest


class MLPredictView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        input_data = request.data.get('input_data')
        if not input_data:
            return Response({"error": "input_data is required"}, status=400)

        ml_request = MLRequest.objects.create(user=request.user, input_data=input_data, result=None)

        return Response({"status": "ok", "request_id": ml_request.id})
