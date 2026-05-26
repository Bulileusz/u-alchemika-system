from django.contrib import admin

from .models import Attraction, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_published', 'published_at', 'created_at']
    list_filter = ['is_published']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_published']


@admin.register(Attraction)
class AttractionAdmin(admin.ModelAdmin):
    list_display = ['name', 'location_name']
    search_fields = ['name', 'location_name']
