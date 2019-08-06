from django.urls import path
from ERP.pedidos import views as v

app_name = 'pedidos'

urlpatterns = [
    path('add/', v.pedido_add, name='pedido_add'),
    ]
