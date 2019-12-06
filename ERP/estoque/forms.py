from django import forms
from ERP.core.models import Item
from .models import Estoque, EstoqueItens


class EstoqueForm(forms.ModelForm):
    class Meta:
        model = Estoque
        fields = ('finaliza', )


class EstoqueItensForm(forms.ModelForm):
    class Meta:
        model = EstoqueItens
        fields = '__all__'


class PedidoItemForm(forms.ModelForm):

    class Meta:
        model = EstoqueItens
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PedidoItemForm, self).__init__(*args, **kwargs)
        # Retorna somente produtos com estoque maior do que zero.
        itens = Item.objects.filter(saldo__gt=0)
        # Remove da lista produtos que já estejam no pedido
        #itens = itens.exclude(estoqueitens__estoque=instance)
        self.fields['produto'].queryset = itens
