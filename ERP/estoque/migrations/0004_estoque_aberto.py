# Generated by Django 2.2.4 on 2019-10-22 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0003_estoque_finaliza'),
    ]

    operations = [
        migrations.AddField(
            model_name='estoque',
            name='aberto',
            field=models.BooleanField(default=True),
        ),
    ]
