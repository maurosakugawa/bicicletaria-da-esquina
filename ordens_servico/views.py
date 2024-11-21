from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import OrdemServico, ProdutoOrdemServico
from estoque.models import Produto
from .forms import OrdemServicoForm, ProdutoOrdemServicoFormSet 
from django.utils import timezone

@login_required
def criar_os(request):
    if request.method == 'POST':
        form = OrdemServicoForm(request.POST)
        formset = ProdutoOrdemServicoFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            ordem_servico = form.save()
            for produto_form in formset:
                produto = produto_form.cleaned_data['produto']
                quantidade = produto_form.cleaned_data['quantidade']
                ProdutoOrdemServico.objects.create(produto=produto, ordem_servico=ordem_servico, quantidade=quantidade)
                produto.quantidade -= quantidade
                produto.save()
            messages.success(request, "Ordem de Serviço criada e estoque atualizado.")
            return redirect('listar_ordens_servico')
    else:
        form = OrdemServicoForm()
        formset = ProdutoOrdemServicoFormSet()
    return render(request, 'ordens_servico/criar_os.html', {'form': form, 'formset': formset})

@login_required
def listar_os(request):
    ordens = OrdemServico.objects.all() if request.user.groups.filter(name="admin").exists() else OrdemServico.objects.filter(funcionario=request.user)
    return render(request, 'ordens_servico/listar_os.html', {'ordens': ordens})

def detalhes_ordem_servico(request, ordem_servico_id):
    # Pega a ordem de serviço pelo ID fornecido
    ordem_servico = get_object_or_404(OrdemServico, id=ordem_servico_id)

    if request.method == 'POST':
        # Se o formulário foi enviado, atualize o status
        novo_status = request.POST.get('status')
        if novo_status in dict(OrdemServico.STATUS_CHOICES).keys():
            ordem_servico.status = novo_status

            # Se o status for 'concluido', remova os produtos do estoque
            if ordem_servico.status == 'concluido' and ordem_servico.produtoordemservico_set.exists():
                for produto_usado in ordem_servico.produtoordemservico_set.all():
                    produto = produto_usado.produto
                    produto.estoque -= produto_usado.quantidade
                    produto.save()

            # Garantir que a data não seja nula
            if not ordem_servico.data:
                ordem_servico.data = timezone.now()
                                                
            ordem_servico.save()
            
            # Redireciona para a página de listagem das ordens de serviço após a atualização
            return redirect('listar_os')
        
    # Passa o objeto ordem_servico para o template
    return render(request, 'ordens_servico/detalhes_ordem_servico.html', {'ordem_servico': ordem_servico})