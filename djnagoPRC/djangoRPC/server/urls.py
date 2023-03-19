from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView

from . import views

urlpatterns = [
    path('data/', views.data, name = 'data'),
    path('new_task/', views.new_task, name = 'new_task'),
    path('data/<int:pk>/', views.remove_item, name='delete'),
    path('home/', views.home, name = 'home'),
    path('', LoginView.as_view(next_page="/data"), name="login"),
    path("logout/", LogoutView.as_view(next_page='/'), name="logout"),
]
