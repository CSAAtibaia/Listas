from django.urls import path
from ERP.listas import views as v

app_name = 'listas'

urlpatterns = [
    path('ativa/', v.lista_itens, name='lista_ativa'),
    ]
