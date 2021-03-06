# Generated by Django 3.1.3 on 2020-11-18 11:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20201118_1055'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cashbackconfig',
            options={'ordering': ['percentual'], 'verbose_name': 'CashBack', 'verbose_name_plural': 'CashBack'},
        ),
        migrations.AlterModelOptions(
            name='cashbackrevendedor',
            options={'ordering': ['data'], 'verbose_name': 'CashBack Revendedor', 'verbose_name_plural': 'CashBack'},
        ),
        migrations.AlterModelOptions(
            name='pedido',
            options={'ordering': ['data'], 'verbose_name': 'Pedido', 'verbose_name_plural': 'Pedidos'},
        ),
        migrations.AlterModelOptions(
            name='revendedor',
            options={'ordering': ['nome'], 'verbose_name': 'Revendedor', 'verbose_name_plural': 'Revendedores'},
        ),
        migrations.AlterModelOptions(
            name='status',
            options={'ordering': ['status'], 'verbose_name': 'Status', 'verbose_name_plural': 'Status'},
        ),
        migrations.AlterModelTable(
            name='cashbackconfig',
            table='cashbackconfig',
        ),
        migrations.AlterModelTable(
            name='cashbackrevendedor',
            table='cashback_revendedor',
        ),
        migrations.AlterModelTable(
            name='pedido',
            table='pedido',
        ),
        migrations.AlterModelTable(
            name='status',
            table='status_pedido',
        ),
    ]
