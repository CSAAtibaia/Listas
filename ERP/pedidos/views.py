from django.shortcuts import render
from django.views.generic import CreateView
from .forms import PedidoForm
from .models import Pedido #, PedidoItem

# Create your views here.


def pedido_add(request):

    template_name='produto_form.html'
    return render(request, template_name)

class PedidoCreate(CreateView):
    model = Pedido
    template_name='pedido_form.html'
    form_class = PedidoForm