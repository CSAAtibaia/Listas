from django import forms
from .models import Estoque, EstoqueItens
from django.forms import widgets


class EstoqueForm(forms.ModelForm):

    class Meta:
        model = Estoque
        fields = ('finaliza', )
        widgets = {
            'finaliza': widgets.DateInput(attrs={'class':'datepicker'}),
            }


class EstoqueItensForm(forms.ModelForm):

    class Meta:
        model = EstoqueItens
        fields = '__all__'


class PedidoForm(forms.ModelForm):

    class Meta:
        model = Estoque
        fields = '__all__'