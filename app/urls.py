from django.urls import path, re_path
from .import views

urlpatterns = [
    path('upload', views.upload, name='upload'),
    # path('configCheckIndex/<run_id>/', views.config_check_index, name='configCheckIndex'),
]