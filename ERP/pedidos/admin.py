from django.contrib import admin
from ERP.pedidos.models import Pedido, PedidoItem

# Register your models here.

class PedidoItemInline(admin.TabularInline):
    model = PedidoItem

class PedidoAdmin(admin.ModelAdmin):
    fields = (('user', 'lista', 'retira'),)
    inlines = [PedidoItemInline,
        ]

admin.site.register(Pedido, PedidoAdmin)