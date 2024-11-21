from django.urls import path
from . import views

urlpatterns = [
    path('criar/', views.criar_os, name='criar_os'),
    path('listar/', views.listar_os, name='listar_os'),
    path('ordem_servico/<int:ordem_servico_id>/', views.detalhes_ordem_servico, name='detalhes_ordem_servico'),
]
