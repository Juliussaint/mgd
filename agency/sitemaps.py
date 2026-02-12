from django.contrib.sitemaps import Sitemap
from agency.models import Project
from blog.models import Post 


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
        # Mengambil Post dari model blog
        return Post.objects.filter(status='published')
    def lastmod(self, obj):
        return obj.updated_at