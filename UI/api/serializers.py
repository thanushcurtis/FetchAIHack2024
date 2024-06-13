from rest_framework import serializers
from .models import (
    SummariseRequest, 
    SummariseResponse, 
    DataMappingRequest, 
    DataMappingResponse, 
    RecommedRequest, 
    RecommendResponse
)

class SummariseRequestSerializer(serializers.ModelSerializer):
    """
    This is a serializer for the summary request
    """

    class Meta:
        model = SummariseRequest
        fields = '__all__'

class SummariseResponseSerializer(serializers.ModelSerializer):
    """
    This is a serializer for the summary response
    """

    class Meta:
        model = SummariseResponse
        fields = '__all__'

class DataMappingRequestSerializer(serializers.ModelSerializer):
    """
    This is a serializer for the mapping request
    """

    class Meta:
        model = DataMappingRequest
        fields = '__all__'

class DataMappingResponseSerializer(serializers.ModelSerializer):
    """
    This is a serializer for the mapping response
    """

    class Meta:
        model = DataMappingResponse
        fields = '__all__'

class RecommedRequestSerializer(serializers.ModelSerializer):
    """
    This is a serializer for the recommending request
    """

    class Meta:
        model = RecommedRequest
        fields = '__all__'

class RecommendResponseSerializer(serializers.ModelSerializer):
    """
    This is a serializer for the recommending response
    """

    class Meta:
        model = RecommendResponse
        fields = '__all__'
