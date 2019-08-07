from django.shortcuts import render
from .models import Lista, ItemLista
from ERP.pedidos.models import Pedido #, PedidoItem
# Create your views here.



def lista_itens(request):
    template_name='lista_ativa.html'
    ativa_id = Lista.objects.get(ativa=True).id
    ativa_tb = ItemLista.objects.filter(lista_id = ativa_id)
    pedidos_tb = Pedido.objects.filter(lista_id = ativa_id)

    #pedidos_item_tb = PedidoItem.objects.filter(Pedido.lista_id = ativa_id)
        #higieniza, retira, item, sum(qtde)
    #ModelName.objects.aggregate(Sum('field_name'))

    context={'ativa_tb': ativa_tb,
                'pedidos_tb': pedidos_tb,
                #'pedidos_item_tb': pedidos_item_tb,
                }
    return render (request, template_name, context)