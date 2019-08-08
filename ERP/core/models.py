from django.db import models
from enum import Enum
#from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.

class TimeStampedModel(models.Model):
    created = models.DateTimeField(
        'Criado em',
        auto_now_add=True,
        auto_now=False
    )
    modified = models.DateTimeField(
        'Modificado em',
        auto_now_add=False,
        auto_now=True,
        blank=True
    )
    class Meta:
        abstract = True

class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        return tuple((x.name, x.value) for x in cls)

class Tipo(ChoiceEnum):
    COTISTA = 'Cotista'
    TRABALHADOR = 'Trabalhador'
    BOLSISTA = 'Bolsista'
    APOIADOR = 'Apoiador'
    PERMUTA = 'Permuta'


class Status(ChoiceEnum):
    ATIVO = 'Ativo'
    INATIVO = 'Inativo'
    AVISO = 'Aviso Prévio'
    SUSPENSO = 'Suspenso'

class Partilha(models.Model):
    partilha = models.CharField('Partilha', max_length=50, unique=True)
    icone = models.CharField('Ícone', max_length=50, blank=True, null=True)

    def __str__(self):
        return self.partilha

class Item(models.Model):
    nome = models.CharField('Item', max_length=50, unique=True)

    class Meta:
        ordering = ('nome',)

    def __str__(self):
        return self.nome

class CoAgri(models.Model):

    user = models.OneToOneField(User,
                                on_delete=models.PROTECT)
    dt_nascimento = models.DateField('Data de Nascimento', null=True, blank=True)
    apelido = models.CharField('Apelido', max_length=50, unique=True, null=True, blank=True)
    tipo = models.CharField('Tipo', choices=Tipo.choices(), default=Tipo.COTISTA, max_length=15, null=True, blank=True)
    status = models.CharField('Status', choices=Status.choices(), default=Status.ATIVO, max_length=15, null=True, blank=True)
    higieniza = models.BooleanField('Higieniza', default=False)
    partilha = models.ForeignKey(Partilha,
                                        on_delete=models.PROTECT, null=True, blank=True)

    telefone = models.BigIntegerField('Telefone', null=True, blank=True)
    credito = models.IntegerField('Crédito Semanal', default = 8)

    class Meta:
        ordering = ('user', 'apelido', )

    def __str__(self):
        if self.apelido:
            x = self.apelido
        elif self.user.first_name:
            x = '{} {}'.format(self.user.first_name, self.user.last_name).strip()
        elif self.user.email:
            x = self.user.email
        else:
            x = self.user.username
        return x

