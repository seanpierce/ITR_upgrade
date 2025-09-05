from rest_framework import serializers
from .models import Show

class ShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = '__all__'
        # fields = ['id', 'name', 'description', 'price', 'in_stock']