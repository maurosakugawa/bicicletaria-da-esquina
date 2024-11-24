# Generated by Django 5.1.2 on 2024-11-24 03:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0001_initial'),
        ('ordens_servico', '0004_rename_ordem_servico_produtoordemservico_ordens_servico_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='produtoordemservico',
            old_name='ordens_servico',
            new_name='ordem_servico',
        ),
        migrations.AlterUniqueTogether(
            name='produtoordemservico',
            unique_together={('produto', 'ordem_servico')},
        ),
    ]
