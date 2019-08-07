from django.shortcuts import render
from .models import Lista, ItemLista
from ERP.pedidos.models import Pedido, PedidoItem
from django.db.models import Sum, F
# Create your views here.



def lista_itens(request):
    template_name='lista_ativa.html'
    ativa_id = Lista.objects.get(ativa=True).id
    ativa_tb = ItemLista.objects.filter(lista_id = ativa_id)
    pedidos_tb = Pedido.objects.filter(lista_id = ativa_id)
    pedidos_item_tb = PedidoItem.objects.filter(pedido__lista_id = ativa_id) #.annotate(higieniza=)
    locais_tb = pedidos_item_tb.values(
            retira = F('pedido__retira'),
            higieniza = F('pedido__user__coagri__higieniza'),
            nomeitem = F('item__item__nome')
        ).order_by(
            'pedido__retira',
            'pedido__user__coagri__higieniza',
            'item__item__nome'
        ).annotate(soma=Sum('qtde'))
    #pedidos_item_tb = PedidoItem.objects.filter(Pedido.lista_id = ativa_id)
        #higieniza, retira, item, sum(qtde)
    #ModelName.objects.aggregate(Sum('field_name'))

    context={'ativa_tb': ativa_tb,
                'pedidos_tb': pedidos_tb,
                'pedidos_item_tb': pedidos_item_tb,
                'locais_tb': locais_tb,
                }
    return render (request, template_name, context)