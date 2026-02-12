from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from agency import views as agency_views
from django.views.static import serve
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap
from agency.sitemaps import StaticViewSitemap, ProjectSitemap, BlogSitemap


sitemaps = {
    'static': StaticViewSitemap,
    'projects': ProjectSitemap,
    'blog': BlogSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('agency.urls')),
    path('blog/', include('blog.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]


print(f"DEBUG MEDIA_ROOT: {settings.MEDIA_ROOT}")

if settings.MEDIA_URL:
    urlpatterns += [
        path(f'{settings.MEDIA_URL.lstrip("/")}<path:path>', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]

handler404 = agency_views.custom_404