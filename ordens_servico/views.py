from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import OrdemServico, ProdutoOrdemServico, F
from estoque.models import Produto
from .forms import OrdemServicoForm, ProdutoOrdemServicoFormSet 
from django.utils import timezone
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import render_to_string

@login_required
def criar_os(request):
    if request.method == "POST":
        form = OrdemServicoForm(request.POST)
        formset = ProdutoOrdemServicoFormSet(request.POST)
        if form.is_valid() and formset.is_valid():

            # Salva a ordem de serviço, atribuindo o usuário logado como funcionário
            ordem_servico = form.save(commit=False)
            ordem_servico.funcionario = request.user  # ID do usuário logado
            ordem_servico.valor_total = 0  # Inicializa o valor total
            ordem_servico.save()
            
            # Salva os produtos associados à ordem de serviço
            for produto_form in formset:
                if produto_form.cleaned_data:  # Ignora formulários vazios no formset
                    quantidade = produto_form.cleaned_data['quantidade']
                    produto = produto_form.cleaned_data['produto']
                    valor_unitario = produto.preco
                    valor_total_produto = quantidade * valor_unitario
                    
                    ProdutoOrdemServico.objects.create(
                        produto=produto,
                        ordem_servico=ordem_servico,
                        quantidade=quantidade,
                        valor=valor_total_produto,
                    )
                    
                    # Incrementa o valor total da OS
                    ordem_servico.valor_total += valor_total_produto
            
            # Salva novamente para registrar o valor total calculado
            ordem_servico.save()
            
            messages.success(request, "Ordem de Serviço criada com sucesso!")
            return redirect('listar_os')
    else:
        form = OrdemServicoForm()
        formset = ProdutoOrdemServicoFormSet()

    return render(request, 'ordens_servico/criar_os.html', {
        'form': form,
        'formset': formset
    })



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

def imprimir_ordem_servico(request, ordem_servico_id):
    # Pega a ordem de serviço pelo ID fornecido
    ordem_servico = get_object_or_404(OrdemServico, id=ordem_servico_id)

    # Obtém os produtos relacionados à ordem de serviço
    produto_usado = ordem_servico.produtoordemservico_set.all()
    
    # Calcula o total geral da ordem de serviço
    total_geral = sum(
        produto.quantidade * produto.produto.preco for produto in produto_usado
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


