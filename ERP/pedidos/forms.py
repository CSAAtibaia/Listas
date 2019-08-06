from django import forms
from .models import Pedido #, PedidoItem

class PedidoForm(forms.ModelForm):

    class Meta:
        model = Pedido
        fields = '__all__'