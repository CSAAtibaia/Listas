from django.db import models
from ERP.core.models import Item
from django.db import connection
# Create your models here.

class Lista(models.Model):
    data_ini = models.DateField()
    data_fim = models.DateField()
    publicada = models.BooleanField(default=False)
    ativa = models.BooleanField(default=False)
    mensagem = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ('-data_ini',)

    def __str__(self):
        return self.data_ini.strftime("%Y-%m-%d")

    def save(self, *args, **kwargs):
        if self.ativa:
            try:
                temp = Lista.objects.get(ativa=True)
                if self != temp:
                    temp.ativa = False
                    temp.save()
            except Lista.DoesNotExist:
                pass
        super(Lista, self).save(*args, **kwargs)
        cursor = connection.cursor()
        cursor.execute("insert into pedidos_pedido (lista_id, user_id, retira, created, modified) " +
                        "select %s, c.user_id, false, NOW(), null from core_coagri c " +
                        "where c.status like 'A%%' and c.user_id not in (select p.user_id from pedidos_pedido p where p.lista_id = %s)",
                        ([self.id], [self.id]))

class ItemLista(models.Model):
    lista   = models.ForeignKey(Lista,
                                    on_delete=models.PROTECT)
    item    = models.ForeignKey(Item,
                                    on_delete=models.PROTECT)
    limite  = models.IntegerField('Limite', default = 1)
    saldo   = models.IntegerField('Saldo', default = 0)

#    def saldo(self):
#        return limite - #query pedido_item filter self.item & pedido filter lista filter ativa true agregate sum qtde

    class Meta:
        verbose_name_plural = "Itens da Lista"
        ordering = ('lista', 'item')
        constraints = [
            models.UniqueConstraint(fields= ['lista','item'],
            name = 'NaoRepetirItememLista')
            ]

    def __str__(self):
        return self.item.nome

    def save(self, *args, **kwargs):
        super(ItemLista, self).save(*args, **kwargs)
        cursor = connection.cursor()
        cursor.execute("insert into pedidos_pedidoitem (pedido_id, item_lista_id, qtde)" +
                        "select distinct p.id, i.id, 0 from listas_itemlista i " +
                        "inner join pedidos_pedido p on (i.lista_id = p.lista_id) " +
                        "where i.lista_id = %s and not EXISTS (" +
                        "select * from pedidos_pedidoitem pi " +
                        "where p.id = pi.pedido_id and i.id = pi.item_lista_id)",
                        [self.id])
