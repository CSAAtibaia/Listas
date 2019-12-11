from django.core.mail import send_mail
from ERP.core.models import CoAgri, Item, Status
from ERP.estoque.models import Estoque
from ERP.settings import DEFAULT_FROM_EMAIL

def email_abertura
	#lista_coagri = CoAgri.objects.filter(status='ATIVO') | CoAgri.objects.filter(status='AVISO')
	lista_coagri = CoAgri.objects.get(user=1)
	lista_emails = list(lista_coagri.values_list('user__email', flat=True))
	lista_itens = Item.objects.filter(saldo__gt=0).values_list('produto', 'saldo', 'preco')
    q = Estoque.objects.filter(aberto=True, movimento='e').aggregate(fim=Max('finaliza'))
    finaliza = q['fim']
    subject = 'Itens Disponibilizados - Finaliza em:%s \n' % (finaliza)
    body = 'Prezad@s, Os itens desta semana já estão disponíveis para Pedido até dia %s.\nLista: \n' % (finaliza, lista_itens)
    for item in lista_itens:
    	body = body + item + '\n'
	body = body.join('\nAtt, \nHorta CSA')

	send_mail(subject, body, DEFAULT_FROM_EMAIL, lista_emails)