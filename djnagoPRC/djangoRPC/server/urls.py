from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView

from . import views

urlpatterns = [
    path('index/', views.data, name='index'),
    path('data/<int:pk>/', views.remove_item, name='delete'),
    path('', LoginView.as_view(next_page="/index"), name="login"),
    path('get_json/', views.get_json, name='get_json'),
    path('get_client/', views.get_client, name='get_client'),
    path("logout/", LogoutView.as_view(next_page='/'), name="logout"),
]
