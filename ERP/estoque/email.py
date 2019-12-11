from django.core.mail import send_mail
from ERP.core.models import CoAgri, Item
from ERP.estoque.models import Estoque
from django.db.models import Max
from ERP.settings import DEFAULT_FROM_EMAIL

def email_abertura():
	lista_coagri = CoAgri.objects.filter(status='ATIVO') | CoAgri.objects.filter(status='AVISO')
	lista_emails = list(lista_coagri.values_list('user__email', flat=True))
	lista_itens = Item.objects.filter(saldo__gt=0).values_list('produto', 'saldo', 'preco')
	q = Estoque.objects.filter(aberto=True, movimento='e').aggregate(fim=Max('finaliza'))
	finaliza = q['fim']
	subject = 'Itens Disponibilizados - Finaliza em:%s' % (finaliza)
	body = 'Prezad@s, Os itens desta semana já estão disponíveis para Pedido até dia %s.\nLista: \n' % (finaliza)
	body = body + 'Nome \t Saldo \t Preço Unitário (R$)\n'
	for item in lista_itens:
		for val in item:
			body = body + str(val) + '\t'
		body = body + '\n'

	body = body + '\nAtt, \nHorta CSA'
	send_mail(subject, body, DEFAULT_FROM_EMAIL, lista_emails)

def body_test():
	lista_itens = Item.objects.filter(saldo__gt=0).values_list('produto', 'saldo', 'preco')
	q = Estoque.objects.filter(aberto=True, movimento='e').aggregate(fim=Max('finaliza'))
	finaliza = q['fim']
	body = 'Prezad@s, Os itens desta semana já estão disponíveis para Pedido até dia %s.\nLista: \n' % (finaliza)
	body = body + 'Nome \t Saldo \t Preço Unitário (R$)\n'
	for item in lista_itens:
		for val in item:
			a = '%-*s' % (25, str(val))
			body = body + a
		body = body + '\n'

	body = body + '\nAtt, \nHorta CSA'
	return body