from rest_framework import serializers
from .models import MLRequest

class MLRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLRequest
        fields = ['id', 'user', 'input_data', 'result', 'created_at']
        read_only_fields = ['id', 'user', 'result', 'created_at']
