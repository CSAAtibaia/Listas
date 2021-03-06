from django.contrib.auth.models import User
from django.db import models
from ERP.core.models import TimeStampedModel, Item
from .managers import ListaManager, PedidoManager
import decimal


MOVIMENTO = (
    ('e', 'entrada'),
    ('s', 'saida'),
    ('f', 'fechamento'),
)


class Estoque(TimeStampedModel):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    movimento = models.CharField(max_length=1, choices=MOVIMENTO, blank=True)
    aberto = models.BooleanField(default=True)
    finaliza = models.DateField(verbose_name='Finaliza em', blank=True, null=True)

    class Meta:
        ordering = ('-finaliza', 'usuario',)

    @property
    def total(self):
        total = list(EstoqueItens.objects.filter(estoque=self, produto__preco=decimal.Decimal(0)).aggregate(models.Sum('quantidade')).values())[0]
        return total

    @property
    def preco_total(self):
        x = decimal.Decimal(0)
        for item in EstoqueItens.objects.filter(estoque=self):
            x = x + (decimal.Decimal(item.quantidade) * item.preco)
        return x

    def __str__(self):
        try:
            fim = self.finaliza.strftime('%d-%m-%Y')
        except:
            fim = None
        try:
            coagri = self.usuario
        except:
            coagri = None
        return '{} - {} - {}'.format(coagri, fim, self.pk)


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

    class Meta:
        ordering = ('pk',)
        unique_together = ('estoque', 'produto',)

    def __str__(self):
        return '{} - {} - {}'.format(self.pk, self.estoque.pk, self.produto)

    @property
    def saldo(self):
        return self.produto.saldo

    @property
    def preco(self):
        return self.produto.preco