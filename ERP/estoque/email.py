from ERP.core.models import CoAgri, Item
from ERP.estoque.models import Estoque
from django.db.models import Max
from ERP.settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def email_abertura():
    lista_coagri = CoAgri.objects.filter(status='ATIVO') | CoAgri.objects.filter(status='AVISO')
    #lista_coagri = lista_coagri.filter(user__is_staff=True)
    #lista_coagri = CoAgri.objects.filter(pk=7)
    lista_emails = list(lista_coagri.values_list('user__email', flat=True))
    lista_itens = Item.objects.filter(saldo__gt=0).order_by('produto')
    q = Estoque.objects.filter(aberto=True, movimento='e').aggregate(fim=Max('finaliza'))
    finaliza = q['fim']

    subject = 'Subject'
    html_message = render_to_string('email_lista_criada.html',
                                    {'finaliza': finaliza, 'lista_itens': lista_itens})
    plain_message = strip_tags(html_message)

    subject = 'Itens Disponibilizados - Finaliza em:%s' % (finaliza)
    send_mail(subject, plain_message, DEFAULT_FROM_EMAIL, lista_emails, html_message=html_message)


def email_fechamento():
    lista_coagri = CoAgri.objects.filter(status='ATIVO') | CoAgri.objects.filter(status='AVISO')
    #lista_coagri = lista_coagri.filter(user__is_staff=True)
    #lista_coagri = CoAgri.objects.filter(pk=7)
    lista_emails = list(lista_coagri.values_list('user__email', flat=True))
    subject = 'Pedidos Encerrados'
    body = 'Encerrado o período de pedidos para a próxima partilha.'
    send_mail(subject, body, DEFAULT_FROM_EMAIL, lista_emails)


def email_pedido(user, mensagem):
    email = [user.email]
    send_mail('Pedido Confirmado', mensagem, DEFAULT_FROM_EMAIL, email)