# Generated by Django 3.0.2 on 2020-01-23 17:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20200122_2002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='fornecedor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='core.Fornecedor'),
        ),
    ]
