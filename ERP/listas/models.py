from django.db import models
from ERP.core.models import Item
# Create your models here.

class Lista(models.Model):
    data_ini = models.DateField()
    data_fim = models.DateField()
    publicada = models.BooleanField()
    mensagem = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ('-data_ini',)

    def __str__(self):
        return self.data_ini.strftime("%Y-%m-%d")

class ItemLista(models.Model):
    lista   = models.ForeignKey(Lista,
                                    on_delete=models.PROTECT)
    item    = models.ForeignKey(Item,
                                    on_delete=models.PROTECT)
    limite  = models.IntegerField('Limite', default = 1)
    saldo   = models.IntegerField('Saldo', default = 0)

    class Meta:
        ordering = ('lista', 'item')

    def __str__(self):
        return self.item.nome