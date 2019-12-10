from django import forms
from .models import Item, Situacao


class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = '__all__'


class SituacaoForm(forms.ModelForm):

    class Meta:
        model = Situacao
        fields = '__all__'
