from django.urls import path
from ERP.core import views as v

app_name = 'core'

urlpatterns = [
    path('', v.index, name='index'),
    path('produto/<int:pk>/json/', v.produto_json, name='produto_json'),
    path('controle/', v.SituacaoUpdate.as_view, name='controle'),
    ]
