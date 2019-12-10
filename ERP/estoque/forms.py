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
                velho = 0
                if EstoqueItens.objects.filter(produto=self.cleaned_data.get('produto'), estoque=e):
                    velho = EstoqueItens.objects.filter(produto=self.cleaned_data.get('produto'), estoque=e).first().quantidade
                    preco = Item.objects.get(produto=self.cleaned_data.get('produto')).preco
                    saldo_item = Item.objects.get(produto=self.cleaned_data.get('produto')).saldo
                novo = self.cleaned_data.get('quantidade')
                saldo = e.usuario.coagri.credito - e.total
                diferenca = novo - velho
                #logger.error(preco)
                if diferenca > saldo and preco < 0.01:
                    raise forms.ValidationError('Quantidade Excede o Crédito Mensal')
                if saldo_item - diferenca < 0:
                    raise forms.ValidationError('Saldo Negativo para o Item')
        return self.cleaned_data.get('quantidade')


    def __init__(self, *args, **kwargs):
        super(PedidoItemForm, self).__init__(*args, **kwargs)
        # Retorna somente produtos com estoque maior do que zero.
        itens = Item.objects.filter(saldo__gt=0)
        try:
            item = Item.objects.filter(pk=self.instance.produto.id)
            itens |= item
        except:
            pass
        self.fields['produto'].queryset = itens
