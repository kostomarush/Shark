from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('tcp/', views.tcp, name='tcp'),
    path('udp/', views.udp, name='udp'),
    path('os/', views.os, name='os'),
    path('aim/', views.data, name='aim'),
    path('not_found/', views.not_found, name='not_found'),
    path('aim/cve_information_aim/<int:pk>/', views.cve_information_aim, name='cve_information_aim'),
    path('segment/', views.segment, name='segment'),
    path('generate_report/<int:pk>/', views.generate_word_report, name='generate_word_report'),
    path('detail_seg/<int:pk>/', views.detail_seg, name='detail_seg'),
    path('aim/data/<int:pk>/', views.remove_item, name='delete'),
    path('segment/<int:pk>/', views.remove_segment, name='segment_delete'),
    path('segment/cve_information/<int:pk>/', views.cve_information, name='cve_information'),
    path('segment/port_information/<int:pk>/', views.port_information, name='port_information'),
    path('aim/port_info_aim/<int:pk>/', views.port_info_aim, name='port_info_aim'),
    path('', LoginView.as_view(next_page="/aim"), name="login"),
    path("logout/", LogoutView.as_view(next_page='/'), name="logout"),
]
