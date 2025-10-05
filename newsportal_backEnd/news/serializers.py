# newsportal_backEnd/news/serializers.py

from rest_framework import serializers
from .models import Article, Category, Location, Image, Video, Comment
from django.conf import settings

# --- Nested Serializers for Related Data ---

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'city')

class ImageSerializer(serializers.ModelSerializer):
    image_file = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ('id', 'caption', 'image_file')

    def get_image_file(self, obj):
        # NOTE: Assumes you have configured MEDIA_URL in settings.py
        if obj.image_file:
            return settings.MEDIA_URL + str(obj.image_file)
        return None


class VideoSerializer(serializers.ModelSerializer):
    video_file = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ('id', 'title', 'video_file')
        
    def get_video_file(self, obj):
        if obj.video_file:
            return settings.MEDIA_URL + str(obj.video_file)
        return None
        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'article', 'author_name', 'content', 'created_at']
        extra_kwargs = {'article': {'required': False}}

# --- Main Article Serializer ---

class ArticleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    location = LocationSerializer(read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    videos = VideoSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = [
            'id', 
            'title', 
            'category', 
            'location', 
            'short_description', 
            'detailed_description', 
            'publication_date', 
            'images', 
            'videos',
            # Fields for comments (if implemented as nested) could go here
        ]