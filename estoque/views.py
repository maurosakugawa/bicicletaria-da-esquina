from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Produto
from .forms import ProdutoForm

@login_required
def listar_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'estoque/listar_produtos.html', {'produtos': produtos})

@login_required
def adicionar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto adicionado com sucesso!')
            return redirect('listar_produtos')
    else:
        form = ProdutoForm()
    return render(request, 'estoque/adicionar_produtos.html', {'form': form})

@login_required
def editar_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
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
def remover_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    produto.delete()
    messages.success(request, 'Produto removido com sucesso!')
    return redirect('listar_produtos')
