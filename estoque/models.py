from django.db import models

class Produto(models.Model):
    CATEGORIA_CHOICES = [
        ('bicicleta', 'Bicicleta'),
        ('peca', 'Peça'),
        ('acessorio', 'Acessório')
    ]

    nome = models.CharField("Nome do Produto", max_length=100)
    categoria = models.CharField("Categoria", max_length=20, choices=CATEGORIA_CHOICES)
    preco = models.DecimalField("Preço", max_digits=10, decimal_places=2)
    quantidade = models.PositiveIntegerField("Quantidade em Estoque", default=0)
    descricao = models.TextField("Descrição do Produto", blank=True)

    def __str__(self):
        return f"{self.nome} ({self.categoria})"
