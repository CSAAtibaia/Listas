from django import forms
from .models import Estoque, EstoqueItens


class EstoqueForm(forms.ModelForm):

    class Meta:
        model = Estoque
        fields = ('finaliza', )


class EstoqueItensForm(forms.ModelForm):

    class Meta:
        model = EstoqueItens
        fields = '__all__'


class PedidoForm(forms.ModelForm):

    class Meta:
        model = Estoque
        fields = '__all__'
