from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('work/', views.work_list, name='work'),
    path('work/<slug:slug>/', views.project_detail, name='work_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('expertise/', views.expertise_list, name='expertise_list'),
    path('service/<slug:slug>/', views.service_detail, name='service_detail'),
]