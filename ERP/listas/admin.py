from django.contrib import admin

from ERP.listas.models import Lista, ItemLista
# Register your models here.

class ItemListaInline(admin.TabularInline):
    model = ItemLista

class ListaAdmin(admin.ModelAdmin):
    list_display = ('data_ini', 'data_fim', 'publicada')
    inlines = [ItemListaInline]
    date_hierarchy = 'data_fim'

admin.site.register(Lista, ListaAdmin)