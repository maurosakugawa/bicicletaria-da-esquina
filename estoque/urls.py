from django.contrib.auth.decorators import login_required, permission_required
from django.urls import path
from . import views

app_name = 'estoque'

urlpatterns = [
    path('', views.listar_produtos, name='listar_produtos'),
    path('adicionar/', views.adicionar_produto, name='adicionar_produto'),
    path('editar/<int:produto_id>/', views.editar_produto, name='editar_produto'),
    path('remover/<int:produto_id>/', views.remover_produto, name='remover_produto'),
    path('api/get_produto_preco/<int:produto_id>/', views.get_produto_preco, name='get_produto_preco'),
]

