# zerar_ordens.py

import os
import django

# Configuração do Django (necessário para acessar os modelos)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seu_projeto.settings')  # Substitua 'seu_projeto' pelo nome do seu projeto
django.setup()

from ordens_servico.models import OrdemServico, ProdutoOrdemServico

def zerar_ordens_servico():
    # Excluir todos os registros da tabela intermediária ProdutoOrdemServico
    ProdutoOrdemServico.objects.all().delete()

    # Excluir todos os registros da tabela OrdemServico
    OrdemServico.objects.all().delete()

    print("Tabelas de Ordens de Serviço e ProdutoOrdemServico foram zeradas com sucesso.")

# Chame a função
zerar_ordens_servico()
