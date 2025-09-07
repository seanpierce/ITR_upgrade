from rest_framework import serializers
from .models import Show

class ShowSerializer(serializers.ModelSerializer):
    happening_now = serializers.ReadOnlyField()
    
    class Meta:
        model = Show
        fields = '__all__'