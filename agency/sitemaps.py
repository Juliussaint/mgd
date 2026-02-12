from django.contrib.sitemaps import Sitemap
from .models import Project, Post, Service

class StaticViewSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

class ProjectSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8
    def items(self):
        return Project.objects.filter(status='published')
    def lastmod(self, obj):
        return obj.created_at

class BlogSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.6
    def items(self):
        return Post.objects.filter(status='published')
    def lastmod(self, obj):
        return obj.updated_at