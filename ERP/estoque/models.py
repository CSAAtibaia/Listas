from django.contrib.auth.models import User
from django.db import models
from ERP.core.models import TimeStampedModel, Item
from .managers import ListaManager, PedidoManager, ListaItensManager


MOVIMENTO = (
    ('e', 'entrada'),
    ('s', 'saida'),
)


class Estoque(TimeStampedModel):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    #nf = models.PositiveIntegerField('nota fiscal', null=True, blank=True)
    movimento = models.CharField(max_length=1, choices=MOVIMENTO, blank=True)
    finaliza = models.DateField(verbose_name='Finaliza em', blank=True, null=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
#        if self.nf:
#            return '{} - {} - {}'.format(self.pk, self.nf, self.created.strftime('%d-%m-%Y'))
        return '{} --- {}'.format(self.pk, self.created.strftime('%d-%m-%Y'))

#    def nf_formated(self):
#        if self.nf:
#            return str(self.nf).zfill(3)
#        return '---'


class Lista(Estoque):

    objects = ListaManager()

    class Meta:
        proxy = True
        verbose_name = 'Lista (Entrada)'
        verbose_name_plural = 'Listas (Entradas)'

    def save(self, *args, **kwargs):
        self.movimento = 'e'
        super(Lista, self).save(*args, **kwargs)


class Pedido(Estoque):

    objects = PedidoManager()

    class Meta:
        proxy = True
        verbose_name = 'Pedido (Saída)'
        verbose_name_plural = 'Pedidos (Saídas)'
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

class ListaItens(EstoqueItens):

    objects = ListaItensManager()

    class Meta:
        proxy = True
        verbose_name = 'Itens da Lista (Saída)'
        verbose_name_plural = 'Itens da Lista (Saídas)'
    def save(self, *args, **kwargs):
        super(ListaItens, self).save(*args, **kwargs)

