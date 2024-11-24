from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

urlpatterns = [
    path('criar/', login_required(views.criar_os), name='criar_os'),
    path('listar/', login_required(views.listar_os), name='listar_os'),
    path('ordem_servico/<int:ordem_servico_id>/', login_required(views.detalhes_ordem_servico), name='detalhes_ordem_servico'),
    path('imprimir_ordem_servico/<int:ordem_servico_id>/', views.imprimir_ordem_servico, name='imprimir_ordem_servico'),
]
