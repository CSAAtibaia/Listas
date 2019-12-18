from django.core.mail import send_mail
from ERP.core.models import CoAgri, Item
from ERP.estoque.models import Estoque
from django.db.models import Max
from ERP.settings import DEFAULT_FROM_EMAIL

def email_abertura():
    lista_coagri = CoAgri.objects.filter(status='ATIVO') | CoAgri.objects.filter(status='AVISO')
    lista_coagri = CoAgri.objects.filter(pk=7)
    lista_emails = list(lista_coagri.values_list('user__email', flat=True))
    lista_itens = Item.objects.filter(saldo__gt=0).values_list('produto', 'saldo', 'preco')
    q = Estoque.objects.filter(aberto=True, movimento='e').aggregate(fim=Max('finaliza'))
    finaliza = q['fim']
    subject = 'Itens Disponibilizados - Finaliza em:%s' % (finaliza)
    body = 'Prezad@s, Os itens desta semana já estão disponíveis para Pedido até dia %s.\nLista: \n' % (finaliza)
    body = body + '%-*s%s\n' % (25, 'Nome', 'Saldo')
    for item in lista_itens:
        for val in item:
            if str(val) == "0.00":
                val=str("")

            a = '%-*s' % (25, str(val))
            body = body + a

        body = body + '\n'

    body = body + '\nAtt, \nHorta CSA'
    send_mail(subject, body, DEFAULT_FROM_EMAIL, lista_emails)
