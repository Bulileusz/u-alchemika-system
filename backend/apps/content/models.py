from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posty'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Attraction(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    location_name = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Atrakcja'
        verbose_name_plural = 'Atrakcje'
        ordering = ['name']

    def __str__(self):
        return self.name
