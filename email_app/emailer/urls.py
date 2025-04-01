from django.urls import path
from . import views

urlpatterns = [
    path('', views.email_form, name='email_form'),
    path('success/', views.email_success, name='email_success'),
    path('history/', views.email_history, name='email_history'),
]