from rest_framework import serializers
from .models import *


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = KafkaData
        fields = '__all__'


class IdSerializer(serializers.Serializer):
    id = serializers.CharField()