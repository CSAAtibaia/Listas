from django.contrib.auth.models import User
from django.db import models
from ERP.core.models import TimeStampedModel, Item
from .managers import ListaManager, PedidoManager
from django.db import connection


MOVIMENTO = (
    ('e', 'entrada'),
    ('s', 'saida'),
)


class Estoque(TimeStampedModel):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    movimento = models.CharField(max_length=1, choices=MOVIMENTO, blank=True)
    aberto = models.BooleanField(default=True)
    finaliza = models.DateField(verbose_name='Finaliza em', blank=True, null=True)

    class Meta:
        ordering = ('-usuario',)

    def __str__(self):
        try:
            fim = self.finaliza.strftime('%d-%m-%Y')
        except:
            fim = None
        return '{} - {} - {}'.format(self.usuario, fim, self.pk)


class Lista(Estoque):

    objects = ListaManager()

    class Meta:
        proxy = True
        verbose_name = 'Lista (Entrada)'
        verbose_name_plural = 'Listas (Entradas)'

    def save(self, *args, **kwargs):
        self.movimento = 'e'
        super(Lista, self).save(*args, **kwargs)
        cursor1 = connection.cursor()
        #insere preemptivo pedido
        cursor1.execute("insert into estoque_estoque (created, modified, movimento, usuario_id, finaliza, aberto) " +
                        "select NOW(), null, 's', c.user_id, %d, True from core_coagri c " +
                        "where c.status like 'A%%' and c.user_id not in (select p.usuario_id from estoque_estoque p " +
                        "where p.aberto = True and p.movimento = 's')",
                        [self.finaliza])

class Pedido(Estoque):

    objects = PedidoManager()

    class Meta:
        proxy = True
        verbose_name = 'Pedido (Saída)'
        verbose_name_plural = 'Pedidos (Saídas)'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cursor2 = connection.cursor()
        cursor2.execute("insert into estoque_estoqueitens (quantidade, saldo, estoque_id, produto_id) " +
                        "select 0, i.estoque, e.id, i.id from core_item i, estoque_estoque e " +
                        "where i.estoque > 0 and i.id not in (select p.produto_id from estoque_estoqueitens p where p.estoque_id = e.id) " +
                        "and e.movimento = 's' and e.aberto = True")

    def save(self, *args, **kwargs):
        self.movimento = 's'
        super(Pedido, self).save(*args, **kwargs)


class EstoqueItens(models.Model):
    estoque = models.ForeignKey(
        Estoque,
        on_delete=models.CASCADE,
        related_name='estoques'
    )
    produto = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    saldo = models.PositiveIntegerField(blank=True)

    class Meta:
        ordering = ('pk',)

    def __str__(self):
        return '{} - {} - {}'.format(self.pk, self.estoque.pk, self.produto)
