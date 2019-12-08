from django import forms
from ERP.core.models import Item
from .models import Estoque, EstoqueItens
import logging

logger = logging.getLogger(__name__)


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

    def clean_quantidade(self):
        for field_name in self.changed_data:
            if field_name == 'quantidade':
                e = self.cleaned_data.get('estoque')
                velho = EstoqueItens.objects.filter(produto=self.cleaned_data.get('produto'), estoque=e).first().quantidade
                novo = self.cleaned_data.get('quantidade')
                saldo = e.usuario.coagri.credito - e.total
                diferenca = novo - velho
                if diferenca > saldo:
                    raise forms.ValidationError('Quantidade Excede o Crédito Mensal')
        return self.cleaned_data.get('quantidade')


    def __init__(self, *args, **kwargs):
        super(PedidoItemForm, self).__init__(*args, **kwargs)
        # Retorna somente produtos com estoque maior do que zero.
        itens = Item.objects.filter(saldo__gt=0)
        # Remove da lista produtos que já estejam no pedido
        #e_id = self.cleaned_data.get('estoque')
        #itens = itens.exclude(estoqueitens__estoque=e_id)
        self.fields['produto'].queryset = itens
