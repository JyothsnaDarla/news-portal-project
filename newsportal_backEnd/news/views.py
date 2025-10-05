# newsportal_backEnd/news/views.py

from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework import filters 
from .models import Article, Category, Comment
from .serializers import ArticleSerializer, CategorySerializer, CommentSerializer
from rest_framework.response import Response
import requests
#from news_portal.translation_utils import translate_to_hindi

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().order_by('-publication_date')
    serializer_class = ArticleSerializer

    def retrieve(self, request, *args, **kwargs):
        # This handles requests for a single article (e.g., /api/articles/1/)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        
        # 🚨 FIX 1: Use the correct function: translate_to_hindi
        # 🚨 FIX 2: Translate fields directly
        
        data['title'] = translate_to_hindi(instance.title)
        data['short_description'] = translate_to_hindi(instance.short_description)
        data['detailed_description'] = translate_to_hindi(instance.detailed_description)
        
        # This view now ALWAYS returns Hindi content for single articles
        return Response(data)

    def list(self, request, *args, **kwargs):
        # This handles requests for the list of articles (e.g., /api/articles/)
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        
        translated_data = []
        for item in serializer.data:
            # 🚨 Translate only the necessary fields for the list view
            item['title'] = translate_to_hindi(item['title'])
            item['short_description'] = translate_to_hindi(item['short_description'])
            translated_data.append(item)
            
        return Response(translated_data)

class CategoryViewSet(viewsets.ModelViewSet):
    """ Handles listing categories. """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CommentListCreateView(generics.ListCreateAPIView):
    """
    Handles listing and creating comments for a specific article.
    """
    serializer_class = CommentSerializer
    permission_classes = [AllowAny] 
    
    # 🚨 CRITICAL FIX: This line MUST be present to disable CSRF/Session checks
    authentication_classes = [] 

    def get_queryset(self):
        # Retrieve the article_id from the URL
        article_id = self.kwargs['article_id']
        return Comment.objects.filter(article__id=article_id).order_by('created_at') # Check for created_at

    def perform_create(self, serializer):
        # Automatically link the new comment to the correct Article instance
        article = Article.objects.get(pk=self.kwargs['article_id'])
        serializer.save(article=article)
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        
        translated_data = []
        for comment in data:
            # Translate the comment content field
            comment['content'] = translate_to_hindi(comment['content'])
            translated_data.append(comment)
            
        return Response(translated_data)
# newsportal_backEnd/news/views.py

# Import the translation utility
#from newsportal_backEnd.news_portal.translation_utils import translate_to_hindi 
# Note: Adjust the import path above if your translation_utils.py is elsewhere
from news_portal.translation_utils import translate_to_hindi
from django.shortcuts import render
# ... other imports

def news_detail_view(request, news_id):
    # 1. Fetch the original news item
    news_item = News.objects.get(id=news_id)
    
    # 2. Get the English title and content
    english_title = news_item.title
    english_content = news_item.content
    
    # 3. Use your API to get the Hindi translations
    hindi_title = translate_to_hindi(english_title)
    hindi_content = translate_to_hindi(english_content)
    
    # 4. Pass BOTH versions to the frontend (or pass the one you need)
    context = {
        'original_title': english_title,
        'translated_title': hindi_title, # This is the translated title you now use
        'content': hindi_content,
        # ... other data
    }
    
    return JsonResponse(data)