from django.contrib import admin
from .models import Lista, Pedido, EstoqueItens


class EstoqueItensInline(admin.TabularInline):
    model = EstoqueItens
    extra = 5


@admin.register(Lista)
class ListaAdmin(admin.ModelAdmin):
    inlines = (EstoqueItensInline,)
    exclude = ('movimento',)
    list_display = ('__str__', 'finaliza')
    #search_fields = ('nf',)
    list_filter = ('usuario',)
    date_hierarchy = 'created'


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    inlines = (EstoqueItensInline,)
    exclude = ('movimento',)
    list_display = ('__str__', 'usuario',)
    #search_fields = ('nf',)
    list_filter = ('usuario',)
    date_hierarchy = 'created'
