# newsportal_backEnd/news/models.py

from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    class Meta:
        verbose_name_plural = "Categories" # Fixes display in Admin
        
    def __str__(self):
        return self.name
    
class Location(models.Model):
    city = models.CharField(max_length=100)
    # ... other fields ...
    def __str__(self):
        return self.city

class Image(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='images')
    image_file = models.ImageField(upload_to='article_images/')
    caption = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return f"Image for {self.article.title}"

class Video(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='videos')
    video_file = models.FileField(upload_to='article_videos/')
    title = models.CharField(max_length=255)
    
    def __str__(self):
        return f"Video: {self.title}"

class Article(models.Model):
    title = models.CharField(max_length=255)
    
    # Replaces 'content' with two descriptive fields
    short_description = models.TextField(help_text="A brief summary for previews (max 250 words).")
    detailed_description = models.TextField()

    publication_date = models.DateTimeField(auto_now_add=True)

    # Foreign Keys for Category and Location
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    
    # REMOVED: keywords, tags, meta_description (as requested)

    def __str__(self):
        return self.title

# Remember to run migrations after adding these fields!

# newsportal_backEnd/news/models.py (Add this section)

class Comment(models.Model):
    # Foreign Key links the comment to a specific Article
    article = models.ForeignKey(
        'Article', 
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    author_name = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.author_name} on {self.article.title[:20]}...'