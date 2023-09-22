from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views

urlpatterns = [
    path('aim/', views.data, name='aim'),
    path('segment/', views.segment, name='segment'),
    path('data/<int:pk>/', views.remove_item, name='delete'),
    path('segment/<int:pk>/', views.remove_segment, name='segment_delete'),
    path('', LoginView.as_view(next_page="/aim"), name="login"),
    path("logout/", LogoutView.as_view(next_page='/'), name="logout"),
]
