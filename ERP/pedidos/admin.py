from django.contrib import admin
from ERP.listas.models import Lista
from ERP.pedidos.models import Pedido, PedidoItem

# Register your models here.

class PedidoItemInline(admin.TabularInline):
    model = PedidoItem

class PedidoAdmin(admin.ModelAdmin):
    inlines = [PedidoItemInline,
        ]

class PedidoUser(admin.ModelAdmin):
    inlines = [PedidoItemInline,
        ]
    exclude = ('user', 'lista',)
    def save_model(self, request, obj, form, change):
        if not change:
            # the object is being created, so set the user
            obj.user = request.user
            obj.lista = Lista.objects.get(ativa=True)
        obj.save()

#admin.site.register(Pedido, PedidoAdmin)
admin.site.register(Pedido, PedidoUser)