# Generated by Django 5.1.2 on 2024-11-08 00:15

import django.db.models.functions.datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordens_servico', '0002_rename_descricao_ordemservico_descricao_servico_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordemservico',
            name='data',
            field=models.DateField(default=django.db.models.functions.datetime.Now, verbose_name='Data do Serviço'),
        ),
    ]
