from django.shortcuts import render, get_object_or_404
from .models import Post, Category

def blog_list(request):
    posts = Post.objects.filter(status='published').order_by('-created_at')
    categories = Category.objects.all()
    return render(request, 'blog/blog_list.html', {'posts': posts, 'categories': categories})

def blog_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    return render(request, 'blog/blog_detail.html', {'post': post})