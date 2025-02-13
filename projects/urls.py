from django.urls import path
from . import views
from .api_views import ProjectsListAPI, ProjectsDetailAPI

app_name = 'projects'

urlpatterns = [
    # Regular views
    path('', views.project_list, name='project_list'),
    path('<int:pk>/', views.project_detail, name='project_detail'),
    # API views
    path('api/projects/', ProjectsListAPI.as_view(), name='api_project_list'),
    path('api/projects/<int:pk>/', ProjectsDetailAPI.as_view(), name='api_project_detail'),
]
