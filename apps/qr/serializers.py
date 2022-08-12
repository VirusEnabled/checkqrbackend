from rest_framework import serializers
from .models import *

class QRValidatorLoginSerializer(serializers.Serializer):
   username = serializers.CharField(max_length=100)
   password = serializers.CharField()