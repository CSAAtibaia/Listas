# Generated by Django 2.2.4 on 2019-08-02 16:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listas', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lista',
            options={'ordering': ('-data_ini',)},
        ),
    ]
