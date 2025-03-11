from django.urls import path
from . import views

app_name = 'demos'

urlpatterns = [
    path('', views.demo_index, name='demo_index'),
    path('<slug:demo_name>/', views.demo_embedded, name='demo_embedded'),
]
