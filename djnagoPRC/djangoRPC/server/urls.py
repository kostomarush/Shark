from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView

from . import views

urlpatterns = [
    path('index/', views.data, name = 'index'),
    path('data/<int:pk>/', views.remove_item, name='delete'),
    path('', LoginView.as_view(next_page="/index"), name="login"),
    path("logout/", LogoutView.as_view(next_page='/'), name="logout"),
]
