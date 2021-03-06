from django.urls import include, path
from ERP.estoque import views as v, lista_view as l


app_name = 'estoque'


entrada_patterns = [
    path('', v.EstoqueEntradaList.as_view(), name='estoque_entrada_list'),
    path('add/', v.estoque_entrada_add, name='estoque_entrada_add'),
]

saida_patterns = [
    path('', v.estoque_saida_list, name='estoque_saida_list'),
    path('sem_pedido/', v.sem_pedido, name='sem_pedido'),
    #path('add/', v.estoque_saida_add, name='estoque_saida_add'),
]

urlpatterns = [
    path('enviar/<int:pk>/', v.pedido_enviar, name='enviar'),
    path('lista/', l.lista_itens, name='lista_ativa'),
    path('lista_print/', l.lista_print, name='lista_print'),
    path('finalizar/', v.finalizar, name='finalizar'),
    path('encerrar/', v.reiniciar, name='encerrar'),
	path('pedido/', v.pedido_edit, name='pedido_update'),
    path('<int:pk>/', v.EstoqueDetail.as_view(), name='estoque_detail'),
    path('entrada/', include(entrada_patterns)),
    path('saida/', include(saida_patterns)),
    path('controle/', v.controle, name='controle'),
]
