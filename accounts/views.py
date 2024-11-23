from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from estoque.models import Produto
from django.http import HttpResponse

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard') 
        else:
            messages.error(request, 'Usuário ou senha incorretos.')
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    request.user.refresh_from_db()
    tem_permissao_estoque = request.user.has_perm('estoque.view_produto')
    
    produtos = Produto.objects.all() if tem_permissao_estoque else None

    return render(request, 'accounts/dashboard.html', {
        'produtos': produtos,
        'tem_permissao_estoque': tem_permissao_estoque,
    })