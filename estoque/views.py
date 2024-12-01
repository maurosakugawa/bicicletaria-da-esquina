from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .models import Produto
from estoque.models import Produto
from .forms import ProdutoForm 
from django.db import IntegrityError
from django.http import JsonResponse

from django.core.exceptions import PermissionDenied

import logging

logger = logging.getLogger(__name__)

@login_required
def dashboard_view(request):
    produtos = Produto.objects.all()
    return render(request, 'accounts/dashboard.html', {
        'produtos': produtos,
    })

@login_required
@permission_required('estoque.view_produto', raise_exception=True)
def listar_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'estoque/listar_produtos.html', {'produtos': produtos})

@login_required
def adicionar_produto(request):
    if not request.user.has_perm('estoque.add_produto'):
        raise PermissionDenied("Você não tem permissão para adicionar produtos.")
    
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto adicionado com sucesso!')
            return redirect('estoque:listar_produtos')
    else:
        form = ProdutoForm()
    
    return render(request, 'estoque/adicionar_produto.html', {'form': form})

@login_required
@permission_required('estoque.change_produto', raise_exception=True)
def editar_produto(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto atualizado com sucesso!')
            return redirect('listar_produtos')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'estoque/editar_produto.html', {'form': form})

@login_required
@permission_required('estoque.delete_produto', raise_exception=True)
def remover_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    try:
        produto.delete()
        messages.success(request, 'Produto removido com sucesso!')
    except IntegrityError:
        messages.error(request, 'Não foi possível remover o produto, ele está associado a outros registros.')
    return redirect('listar_produtos')

def get_produto_preco(request, produto_id):
    try:
        produto = Produto.objects.get(id=produto_id)
        response_data = {
            'produto': produto.nome,
            'quantidade': produto.quantidade,
            'preco': str(produto.preco), 
        }
        return JsonResponse(response_data)
    except Produto.DoesNotExist:
        return JsonResponse({'error': 'Produto não encontrado no estoque.'}, status=404)
