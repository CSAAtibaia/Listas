from django import forms
from .models import Estoque, EstoqueItens #, ListaItens

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
        self.fields['estoque'].queryset = EstoqueItens.objects.filter(saldo__gt=0)