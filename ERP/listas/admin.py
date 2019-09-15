from django.contrib import admin

from ERP.listas.models import Lista, ItemLista
# Register your models here.

class ItemListaInline(admin.TabularInline):
    model = ItemLista
    readonly_fields = ('saldo',)

class ListaAdmin(admin.ModelAdmin):
    list_display = ('data_ini', 'data_fim', 'publicada', 'ativa')
    inlines = [ItemListaInline]
    date_hierarchy = 'data_fim'

admin.site.register(Lista, ListaAdmin)