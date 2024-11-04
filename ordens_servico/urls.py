from django.urls import path
from . import views

urlpatterns = [
    path('criar/', views.criar_os, name='criar_os'),
    path('listar/', views.listar_os, name='listar_os'),
]
