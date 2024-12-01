from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .models import OrdemServico, ProdutoOrdemServico, F
from estoque.models import Produto
from .forms import OrdemServicoForm, ProdutoOrdemServicoFormSet 
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from xhtml2pdf import pisa
from django.template.loader import render_to_string
from django.db import transaction
from django.urls import reverse

@login_required
@permission_required('ordens_servico.add_ordemservico', raise_exception=True)
def criar_os(request):
    if request.method == "POST":
        ordem_servico_form = OrdemServicoForm(request.POST)
        formset = ProdutoOrdemServicoFormSet(request.POST)

        # Valida os formulários
        if ordem_servico_form.is_valid() and formset.is_valid():
            # Salva a ordem de serviço, mas não comita ainda (sem salvar no banco)
            ordem_servico = ordem_servico_form.save(commit=False)
            ordem_servico.funcionario = request.user
            
            # Salvar a ordem de serviço primeiro
            ordem_servico.save()

            valor_total = 0
            for form in formset:
                produto = form.cleaned_data.get('produto')
                quantidade = form.cleaned_data.get('quantidade')

                if produto and quantidade:
                    produto_ordem_servico = form.save(commit=False)
                    produto_ordem_servico.ordem_servico = ordem_servico                    
                    produto_ordem_servico.save()

                    valor_total += produto.preco * quantidade

            # Atribui o valor total calculado
            ordem_servico.valor_total = valor_total
            ordem_servico.save()

            return redirect('ordens_servico:listar_os')

        else:
            pass
    else:
        ordem_servico_form = OrdemServicoForm()
        formset = ProdutoOrdemServicoFormSet()

    return render(request, 'ordens_servico/criar_os.html', {
        'ordem_servico_form': ordem_servico_form,
        'formset': formset,
    })



@login_required
@permission_required('ordens_servico.view_ordemservico', raise_exception=True)
def listar_os(request):
    ordens = OrdemServico.objects.all() if request.user.groups.filter(name="admin").exists() else OrdemServico.objects.filter(funcionario=request.user)
    return render(request, 'ordens_servico/listar_os.html', {'ordens': ordens})

@login_required
@permission_required('ordens_servico.view_produtoordemservico', raise_exception=True)
def detalhes_ordem_servico(request, ordem_servico_id):
    # Pega a ordem de serviço pelo ID fornecido
    ordem_servico = get_object_or_404(OrdemServico, id=ordem_servico_id)

    if request.method == 'POST':
        # Se o formulário foi enviado, atualize o status
        novo_status = request.POST.get('status')
        if novo_status in dict(OrdemServico.STATUS_CHOICES).keys():
            ordem_servico.status = novo_status

            if ordem_servico.status == 'concluido' and ordem_servico.produtoordemservico_set.exists():
                for produto_usado in ordem_servico.produtoordemservico_set.all():
                    produto = produto_usado.produto
                    produto.quantidade -= produto_usado.quantidade
                    produto.save()

            # Garantir que a data não seja nula
            if not ordem_servico.data:
                ordem_servico.data = timezone.now()
                                                
            ordem_servico.save()
            
            # Redireciona para a página de listagem das ordens de serviço após a atualização
            return redirect('ordens_servico:listar_os')
        
    # Passa o objeto ordem_servico para o template
    return render(request, 'ordens_servico/detalhes_ordem_servico.html', {'ordem_servico': ordem_servico})

def imprimir_ordem_servico(request, ordem_servico_id):
    # Pega a ordem de serviço pelo ID fornecido
    ordem_servico = get_object_or_404(OrdemServico, id=ordem_servico_id)

    # Obtém os produtos relacionados à ordem de serviço
    produto_usado = ordem_servico.produtoordemservico_set.all()
    
    # Calcula o total geral da ordem de serviço
    total_geral = sum(
        produto.quantidade * produto.valor for produto in produto_usado
    )

    # Renderiza o template HTML para o relatório
    context = {
        'ordem_servico': ordem_servico,
        'produto_usado': produto_usado,
        'total_geral': total_geral,
    }
    html = render_to_string('ordens_servico/relatorio_ordem_servico.html', context)

    # Cria um objeto HttpResponse com tipo de conteúdo de PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=ordem_servico_{ordem_servico.id}.pdf'

    # Usa o xhtml2pdf para gerar o PDF a partir do HTML renderizado
    pisaStatus = pisa.CreatePDF(html, dest=response)

    # Se ocorrer algum erro durante a conversão, exibe o erro
    if pisaStatus.err:
        return HttpResponse('Erro ao gerar o PDF', status=500)

    return response

@login_required
def atualizar_status_ordem_servico(request, ordem_servico_id):
    ordem_servico = get_object_or_404(OrdemServico, id=ordem_servico_id)
    
    if request.method == 'POST':
        novo_status = request.POST.get('status')
        ordem_servico.status = novo_status
        ordem_servico.save() 

    return redirect('ordens_servico:detalhes_ordem_servico', ordem_servico_id=ordem_servico.id)

@login_required
@permission_required('ordens_servico.delete_ordemservico', raise_exception=True)
def excluir_ordem_servico(request, pk):
    ordem_servico = get_object_or_404(OrdemServico, pk=pk)

    if request.method == "POST":
        ordem_servico.delete()
        messages.success(request, "Ordem de Serviço excluída com sucesso!")
        return redirect(reverse('ordens_servico:listar_os')) 

    return render(request, 'ordens_servico/confirmar_exclusao.html', {'ordem_servico': ordem_servico})

