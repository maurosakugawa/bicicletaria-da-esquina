from django.db.models import signals
from django.dispatch import receiver
from .models import OrdemServico

@receiver(signals.post_save, sender=OrdemServico)
def remover_produto_estoque(sender, instance, created, **kwargs):
    if instance.status == 'concluido':  # Quando o status for concluído
        for produto_usado in instance.produtoordemservico_set.all():
            produto = produto_usado.produto
            produto.quantidade -= produto_usado.quantidade  # Atualiza o estoque
            produto.save()


