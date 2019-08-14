from django import forms
from .models import Pedido, PedidoItem

class PedidoForm(forms.ModelForm):

    class Meta:
        model = Pedido
        fields = '__all__'

class PedidoItemForm(forms.ModelForm):

    class Meta:
        model = PedidoItem
        fields = '__all__'