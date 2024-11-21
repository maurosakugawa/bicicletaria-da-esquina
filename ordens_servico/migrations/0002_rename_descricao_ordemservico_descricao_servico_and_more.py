# migrations/000X_rename_funcionario.py
import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def set_funcionario_default(apps, schema_editor):
    User = apps.get_model('auth', 'User')  # Obtém o modelo User
    try:
        # Buscar o 'Funcionário Desconhecido' pelo nome (ou pelo ID, se preferir)
        funcionario = User.objects.get(username='Funcionario Desconhecido')  # ou use o ID diretamente
    except User.DoesNotExist:
        # Caso o usuário 'Funcionario Desconhecido' não exista, você pode lidar com o erro ou criar o usuário
        print("Funcionário Desconhecido não encontrado.")
        return

    # Atualizar as ordens_servico com 'funcionario=None' para o funcionario correto
    OrdemServico = apps.get_model('ordens_servico', 'OrdemServico')
    for ordem in OrdemServico.objects.filter(funcionario__isnull=True):
        ordem.funcionario = funcionario
        ordem.save()


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0001_initial'),
        ('ordens_servico', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='ordemservico',
            old_name='descricao',
            new_name='descricao_servico',
        ),
        migrations.RemoveField(
            model_name='ordemservico',
            name='data_criacao',
        ),
        migrations.RemoveField(
            model_name='ordemservico',
            name='data_finalizacao',
        ),
        migrations.RemoveField(
            model_name='ordemservico',
            name='valor',
        ),
        migrations.AddField(
            model_name='ordemservico',
            name='cliente',
            field=models.CharField(default='Cliente Desconhecido', max_length=100, verbose_name='Nome do Cliente'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ordemservico',
            name='data',
            field=models.DateField(default=datetime.datetime(2024, 11, 7, 0, 9, 7, 53764, tzinfo=datetime.timezone.utc), verbose_name='Data do Serviço'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ordemservico',
            name='valor_total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Valor Total'),
        ),
        migrations.AlterField(
            model_name='ordemservico',
            name='funcionario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ordens_servico', to=settings.AUTH_USER_MODEL, verbose_name='Funcionário'),
        ),
        migrations.AlterField(
            model_name='ordemservico',
            name='status',
            field=models.CharField(choices=[('pendente', 'Pendente'), ('concluido', 'Concluído'), ('cancelado', 'Cancelado')], default='pendente', max_length=20, verbose_name='Status'),
        ),
        migrations.CreateModel(
            name='ProdutoOrdemServico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.PositiveIntegerField(verbose_name='Quantidade Utilizada')),
                ('ordem_servico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ordens_servico.ordemservico')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='estoque.produto')),
            ],
            options={
                'unique_together': {('produto', 'ordem_servico')},
            },
        ),
        migrations.AddField(
            model_name='ordemservico',
            name='produtos_usados',
            field=models.ManyToManyField(blank=True, through='ordens_servico.ProdutoOrdemServico', to='estoque.produto'),
        ),
        # Rodar a função para definir o funcionário
        migrations.RunPython(set_funcionario_default),
    ]
