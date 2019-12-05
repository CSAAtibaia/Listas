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
        self.fields['produto'].queryset = Item.objects.filter(saldo__gt=0)

    def save(self, *args, **kwargs):
        self.instance.saldo = self.cleaned_data['saldo']
        self.instance.preco = self.cleaned_data['preco']
        return super().save(*args, **kwargs)