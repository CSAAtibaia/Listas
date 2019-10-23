from django import forms
from .models import Estoque, EstoqueItens
from django.db import connection


class EstoqueForm(forms.ModelForm):

    class Meta:
        model = Estoque
        fields = ('finaliza', 'movimento',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.fields['movimento'] == 's':
	        cursor = connection.cursor()
	        #insere preemptivo pedido item
	        cursor.execute("insert into estoque_estoqueitens (quantidade, saldo, estoque_id, produto_id) " +
							"select 0, i.estoque, %s, i.id from core_item i " +
							"where i.estoque > 0 and i.id not in (select p.produto_id from estoque_estoqueitens p " +
							"where p.estoque_id = %s)",
	                        ([self.id]))


class EstoqueItensForm(forms.ModelForm):

    class Meta:
        model = EstoqueItens
        fields = '__all__'