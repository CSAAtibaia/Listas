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
                        "select %i, c.user_id, false, NOW(), null from core_coagri c " +
                        "where c.status like 'A%%' and c.user_id not in (select p.user_id from pedidos_pedido p where p.lista_id = %i)",
                        [self.id])

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