from django.shortcuts import render
from .models import Lista, ItemLista
# Create your views here.

def lista_itens(request):
    template_name='lista_ativa.html'
    lista_ativa = Lista.objects.get(ativa=True)
    objetcs = ItemLista.objects.filter(lista_id = lista_ativa.id)

    context={'object_list': objetcs}
    return render (request, template_name, context)