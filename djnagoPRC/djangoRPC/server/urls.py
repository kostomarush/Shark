from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('data/', views.data, name = 'data'),
    path('home/', views.home, name = 'home'),
    path('', LoginView.as_view(next_page="/data"), name="login"),
    path("logout/", LogoutView.as_view(next_page='/'), name="logout"),
]
