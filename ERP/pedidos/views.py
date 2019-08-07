from django.shortcuts import render
from django.views.generic import CreateView
from .forms import PedidoForm
from ERP.listas.models import Lista
from .models import Pedido #, PedidoItem

# Create your views here.


def pedido_add(request):

    template_name='produto_form.html'
    return render(request, template_name)

class PedidoCreate(CreateView):
    model = Pedido
    ativa_id = Lista.objects.get(ativa=True).id

    template_name='pedido_form.html'
    form_class = PedidoForm