# external_courses/serializers.py
from rest_framework import serializers

class ExternalCourseSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    difficulty = serializers.CharField()
    estimated_duration = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
