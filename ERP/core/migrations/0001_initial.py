# Generated by Django 2.2.4 on 2019-08-02 13:56

import ERP.core.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50, unique=True, verbose_name='Item')),
            ],
            options={
                'ordering': ('nome',),
            },
        ),
        migrations.CreateModel(
            name='Partilha',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('partilha', models.CharField(max_length=50, unique=True, verbose_name='Partilha')),
            ],
        ),
        migrations.CreateModel(
            name='CoAgri',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dt_nascimento', models.DateField(blank=True, null=True, verbose_name='Data de Nascimento')),
                ('apelido', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='Apelido')),
                ('tipo', models.CharField(blank=True, choices=[('COTISTA', 'Cotista'), ('TRABALHADOR', 'Trabalhador'), ('BOLSISTA', 'Bolsista'), ('APOIADOR', 'Apoiador'), ('PERMUTA', 'Permuta')], default=ERP.core.models.Tipo('Cotista'), max_length=15, null=True, verbose_name='Tipo')),
                ('status', models.CharField(blank=True, choices=[('ATIVO', 'Ativo'), ('INATIVO', 'Inativo'), ('AVISO', 'Aviso Prévio'), ('SUSPENSO', 'Suspenso')], default=ERP.core.models.Status('Ativo'), max_length=15, null=True, verbose_name='Status')),
                ('higieniza', models.BooleanField(default=False, verbose_name='Higieniza')),
                ('telefone', models.BigIntegerField(blank=True, null=True, verbose_name='Telefone')),
                ('credito', models.IntegerField(default=8, verbose_name='Crédito Semanal')),
                ('partilha', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.Partilha')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('apelido', 'user'),
            },
        ),
    ]
