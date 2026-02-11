from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from agency import views as agency_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('agency.urls')),
    path('blog/', include('blog.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = agency_views.custom_404