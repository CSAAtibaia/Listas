from django.db import models
from django.contrib.auth.models import User
from ERP.core.models import TimeStampedModel #, Item
from ERP.listas.models import Lista, ItemLista
# Create your models here.


class Pedido(TimeStampedModel):
    user  = models.ForeignKey(User,
                                    on_delete=models.PROTECT)
    lista   = models.ForeignKey(Lista,
                                    on_delete=models.PROTECT,
                                    limit_choices_to={'ativa': True},
                                    )
    retira  = models.BooleanField(default=False)


    class Meta:
        ordering = ('-created',)
        constraints = [
            models.UniqueConstraint(fields= ['user','lista'],
            name = 'UmPedidoporCoAgri')
            ]

    def __str__(self):
        return '{} / {} / {}'.format(self.user.username, self.pk, self.created.strftime('%d-%m-%Y'))

ativa_id = Lista.objects.get(ativa=True).id

class PedidoItem(models.Model):
    pedido  = models.ForeignKey(Pedido,
                                    on_delete=models.PROTECT)

    item  = models.ForeignKey(ItemLista,
                                    on_delete=models.PROTECT,
                                    limit_choices_to={'lista_id': ativa_id},
                                    )

    qtde    = models.IntegerField('Qtde', default = 1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields= ['pedido','item'],
            name = 'NaoRepetirItememPedido')
            ]
    def __str__(self):
        return '{}/{}'.format(self.pedido, self.item)


