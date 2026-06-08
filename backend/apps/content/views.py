from django.shortcuts import render, get_object_or_404

from .models import Post, Attraction

def post_list(request):
    posts = Post.objects.filter(is_published=True)
    return render(request, 'content/post_list.html', {'posts': posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, is_published=True)
    return render(request, 'content/post_detail.html', {'posts': posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, is_published=True)
    return render(request, 'content/post_detail.html', {'post': post})

def attraction_list(request):
    attractions = Attraction.objects.all()
    return render(request, 'content/attraction_list.html', {'attractions': attractions})

