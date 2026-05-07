from django.urls import path
from django.views.generic import TemplateView
from . import views
from .views import free_consultation


urlpatterns = [
	path('', views.home, name="home"),
	path('contact/', views.contact, name="contact"),
	path('about/', views.about, name="about"),
	path('pricing/', views.pricing, name="pricing"),
	path('service/', views.service, name="service"),
	path('appointment/', views.appointment, name="appointment"),
    path("free-consultation/", free_consultation, name="free_consult"),
    path('blog-details/1/', views.blog1, name='blog1'),
    path('blog-details/2/', views.blog2, name='blog2'),
    path('blog-details/3/', views.blog3, name='blog3'),
    path('privacy-policy/', TemplateView.as_view(template_name='privacy_policy.html'), name='privacy_policy'),



]
