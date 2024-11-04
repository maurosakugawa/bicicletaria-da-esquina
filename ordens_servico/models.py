from django.db import models
from django.contrib.auth.models import User


class OrdemServico(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('em_andamento', 'Em Andamento'),
        ('finalizado', 'Finalizado'),
    ]




    funcionario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'groups__name': 'funcionario'})
    descricao = models.TextField("Descrição do Serviço")
    valor = models.DecimalField("Valor", max_digits=10, decimal_places=2)
    status = models.CharField("Status", max_length=15, choices=STATUS_CHOICES, default='pendente')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_finalizacao = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"OS #{self.id} - {self.descricao[:20]}"
    