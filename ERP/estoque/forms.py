from django import forms
import logging
from .models import Estoque, EstoqueItens #, ListaItens

logger = logging.getLogger(__name__)

class EstoqueForm(forms.ModelForm):

    class Meta:
        model = Estoque
        fields = ('finaliza',)


class EstoqueItensForm(forms.ModelForm):

    #def __init__(self, *args, **kwargs):
    #   super(EstoqueItensForm, self).__init__(*args, **kwargs)
    #   self.fields['saldo'].widget.attrs['readonly'] = True

    class Meta:
        model = EstoqueItens
        fields = '__all__'

class ListaItensForm(forms.ModelForm):

    #def __init__(self, *args, **kwargs):
    #   super(EstoqueItensForm, self).__init__(*args, **kwargs)
    #   self.fields['saldo'].widget.attrs['readonly'] = True

    class Meta:
        model = EstoqueItens
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.error(self)
        logger.error(args)
        logger.error(kwargs)
        #self.fields['produto'].queryset = EstoqueItens.objects.filter(saldo__gt=0).values('produto', 'produto__produto')
        self.fields['produto'].choices= [(EstoqueItens.produto.id, EstoqueItens.produto.produto) for produto in EstoqueItens.objects.filter(saldo__gt=0)]