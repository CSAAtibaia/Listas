from django.contrib import admin
from .models import Lista, Pedido, EstoqueItens


class EstoqueItensInline(admin.TabularInline):
    model = EstoqueItens
    extra = 0


@admin.register(Lista)
class ListaAdmin(admin.ModelAdmin):
    inlines = (EstoqueItensInline,)
    list_display = ('__str__', 'usuario',)
    #search_fields = ('nf',)
    list_filter = ('usuario',)
    date_hierarchy = 'created'


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    inlines = (EstoqueItensInline,)
    list_display = ('__str__', 'usuario',)
    #search_fields = ('nf',)
    list_filter = ('usuario',)
    date_hierarchy = 'created'
