from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import OrdemServico
from .forms import OrdemServicoForm
from django.utils import timezone

@login_required
def criar_os(request):
    if request.method == 'POST':
        form = OrdemServicoForm(request.POST)
        if form.is_valid():
            os = form.save(commit=False)
            os.funcionario = request.user
            os.save()
            messages.success(request, 'Ordem de serviço criada com sucesso!')
            return redirect('listar_os')
    else:
        form = OrdemServicoForm()
    return render(request, 'ordens_servico/criar_os.html', {'form': form})

@login_required
def listar_os(request):
    ordens = OrdemServico.objects.all() if request.user.groups.filter(name="admin").exists() else OrdemServico.objects.filter(funcionario=request.user)
    return render(request, 'ordens_servico/listar_os.html', {'ordens': ordens})

