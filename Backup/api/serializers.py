from rest_framework import serializers
from .models import SummariseRequest, SummariseResponse, DataMappingRequest, DataMappingResponse, RecommedRequest, RecommendResponse

class SummariseRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SummariseRequest
        fields = '__all__'

class SummariseResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SummariseResponse
        fields = '__all__'

class DataMappingRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataMappingRequest
        fields = '__all__'

class DataMappingResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataMappingResponse
        fields = '__all__'

class RecommedRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecommedRequest
        fields = '__all__'

class RecommendResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecommendResponse
        fields = '__all__'
