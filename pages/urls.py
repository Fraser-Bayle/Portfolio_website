from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('technologies/', views.technologies, name='technologies'),
    path('easter_egg/', views.easter_egg, name='easter_egg'),
]
