from django.shortcuts import render
from .models import Lista, ItemLista
from ERP.pedidos.models import Pedido
# Create your views here.

def lista_itens(request):
    template_name='lista_ativa.html'
    ativa_id = Lista.objects.get(ativa=True).id
    ativa_tb = ItemLista.objects.filter(lista_id = ativa_id)
    pedidos = Pedido.objects.filter(lista_id = ativa_id)


    context={'ativa_tb': ativa_tb,
                'pedidos': pedidos,
                }
    return render (request, template_name, context)