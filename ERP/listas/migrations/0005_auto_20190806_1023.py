# Generated by Django 2.2.4 on 2019-08-06 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listas', '0004_auto_20190805_1454'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='itemlista',
            constraint=models.UniqueConstraint(fields=('lista', 'item'), name='NaoRepetirItememLista'),
        ),
    ]