from django.db import models


class ListaManager(models.Manager):

    def get_queryset(self):
        return super(ListaManager, self).get_queryset().filter(movimento='e')


class PedidoManager(models.Manager):

    def get_queryset(self):
        return super(PedidoManager, self).get_queryset().filter(movimento='s')