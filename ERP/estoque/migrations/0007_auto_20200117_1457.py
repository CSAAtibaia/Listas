# Generated by Django 3.0.2 on 2020-01-17 16:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20200117_1457'),
        ('estoque', '0006_auto_20191129_1133'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='estoqueitens',
            unique_together={('estoque', 'produto')},
        ),
    ]
