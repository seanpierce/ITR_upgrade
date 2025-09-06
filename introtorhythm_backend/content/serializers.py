from rest_framework import serializers
from .models import MarqueeText, About

class MarqueeTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarqueeText
        fields = '__all__'

class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = '__all__'