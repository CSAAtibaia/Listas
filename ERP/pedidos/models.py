from django.db import models
from django.contrib.auth.models import User
from ERP.core.models import Item, TimeStampedModel
from ERP.listas.models import Lista
# Create your models here.


class Pedido(TimeStampedModel):
    user  = models.ForeignKey(User,
                                    on_delete=models.PROTECT)
    lista   = models.ForeignKey(Lista,
                                    on_delete=models.PROTECT)
    retira  = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} / {} / {}'.format(self.user.username, self.pk, self.created.strftime('%d-%m-%Y'))


class PedidoItem(models.Model):
    pedido  = models.ForeignKey(Pedido,
                                    on_delete=models.PROTECT)
    item    = models.ForeignKey(Item,
                                    on_delete=models.PROTECT)
    qtde    = models.IntegerField('Qtde', default = 1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields= ['pedido','item'],
            name = 'NaoRepetirItememPedido')
            ]
    def __str__(self):
        return '{}/{}'.format(self.pedido, self.item)