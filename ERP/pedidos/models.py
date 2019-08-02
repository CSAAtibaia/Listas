from django.db import models
from ERP.core.models import CoAgri, Item
from ERP.listas.models import Lista
# Create your models here.


class Pedido(models.Model):
    coagri  = models.ForeignKey(CoAgri,
                                    on_delete=models.PROTECT)
    lista   = models.ForeignKey(Lista,
                                    on_delete=models.PROTECT)
    retira  = models.BooleanField(default=False)

    def __str__(self):
        return self.coagri + ' ' + self.lista


class PedidoItem(models.Model):
    pedido  = models.ForeignKey(Pedido,
                                    on_delete=models.PROTECT)
    item    = models.ForeignKey(Item,
                                    on_delete=models.PROTECT)
    qtde    = models.IntegerField('Qtde', default = 1)

    def __str__(self):
        return self.pedido + ' ' + self.item