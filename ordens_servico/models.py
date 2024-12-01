from django.db import models
from django.contrib.auth.models import User
from django.db.models import F
from django.db.models.functions import Now
from django.utils.timezone import now


class OrdemServico(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
    ]

    cliente = models.CharField("Nome do Cliente", max_length=100)
    descricao_servico = models.TextField("Descrição do Serviço")
    data = models.DateTimeField("Data do Serviço", default=now)
    status = models.CharField("Status", max_length=20, choices=STATUS_CHOICES, default='pendente')
    valor_total = models.DecimalField("Valor Total", max_digits=10, decimal_places=2, blank=True, null=True)
    produtos_usados = models.ManyToManyField('estoque.Produto', through='ProdutoOrdemServico', blank=True)

    funcionario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Funcionário", related_name="ordens_servico")

    def __str__(self):
        return f"Ordem de Serviço #{self.id} - {self.cliente}"
    
    def atualizar_valor_total(self):
        """Método para atualizar o valor total da ordem de serviço"""
        self.valor_total = sum(produto.valor for produto in self.produtoordemservico_set.all())
        self.save()   

class ProdutoOrdemServico(models.Model):
    produto = models.ForeignKey('estoque.Produto', on_delete=models.CASCADE, related_name='ordens_servico_produtos')  # Usar a string 'Produto'
    ordem_servico = models.ForeignKey(OrdemServico, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField("Quantidade Utilizada")
    
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        """Sobrescreve o método save para calcular o valor do produto automaticamente."""
        self.valor = self.produto.preco * self.quantidade  # Calcula o valor automaticamente
        super().save(*args, **kwargs)
        
    class Meta:
        unique_together = ('produto', 'ordem_servico')
