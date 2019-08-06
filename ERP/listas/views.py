from django.shortcuts import render
from .models import Lista, ItemLista
# Create your views here.

def lista_itens(request):
    template_name='lista_ativa.html'
    ativa_id = Lista.objects.get(ativa=True).id
    objetcs = ItemLista.objects.filter(lista_id = ativa_id)

    context={'object_list': objetcs}
    return render (request, template_name, context)