# Generated by Django 3.1.3 on 2020-11-18 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20201118_1328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='revendedor',
            name='senha',
            field=models.CharField(max_length=100, verbose_name='Senha'),
        ),
    ]
