from django.urls import path
from . import views
from .api_views import ProjectsListAPI, ProjectsDetailAPI

app_name = 'projects'

urlpatterns = [
    path('projects/', ProjectsListAPI.as_view(), name='project_list'),
    path('projects/<int:pk>/', ProjectsDetailAPI.as_view(), name='project_detail'),
]