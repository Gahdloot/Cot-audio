from .models import Minister, Content, Events
from rest_framework import serializers




class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ['id', 'minister_name', 'name', 'content', 'image', 'event_name', 'times_played']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Minister
        fields = ['id', 'name', 'content', 'picture', 'times_played', 'description', 'publish']


class HomePageMinisters(serializers.ModelSerializer):
    class Meta:
        model = Minister
        fields = ['name', 'id', 'picture']


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ['name', 'times_played']