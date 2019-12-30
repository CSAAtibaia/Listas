from django.core.management.base import BaseCommand
from ERP.estoque.models import Estoque
from ERP.estoque.views import recalcular_estoque
from ERP.estoque.email import email_fechamento
from django.utils.timezone import datetime

class Command(BaseCommand):
    help = 'Fechamento automático na data de Finalizar'

    def handle(self, *args, **options):
        today = datetime.today()
        lista = Estoque.objects.filter(finaliza__lte=today, aberto=True)
        for estoque in lista:
            estoque.aberto=False
            estoque.save()
            self.stdout.write(self.style.SUCCESS('Pedidos fechados com sucesso "%s"' % estoque))
        
        if lista:    
            email_fechamento()
            recalcular_estoque()
