from django.shortcuts import render
from .models import Lista, ItemLista
from ERP.pedidos.models import PedidoItem #, Pedido
from django.db.models import Sum, F, CharField, Case, When, Value #, Q
from django.db.models.functions import Coalesce, Cast
# Create your views here.



def lista_itens(request):
    template_name='lista_ativa.html'
    ativa_id = Lista.objects.get(ativa=True).id
    ativa_tb = ItemLista.objects.filter(lista_id = ativa_id)

    pedidos_item_tb = PedidoItem.objects.filter(pedido__lista_id = ativa_id)

    coagris_tb = pedidos_item_tb.values(
            higieniza = F('pedido__user__coagri__higieniza'),
            coagri = Coalesce(
                Cast('pedido__user__coagri__apelido', CharField()),
                Cast('pedido__user__username', CharField())
                ),
            nomeitem = F('item__item__nome'),
            total = F('qtde')
        ).annotate(entrega=Case(
                        When(pedido__retira=True, then=Value("Retira")),
                        default=F('pedido__user__coagri__partilha__partilha'),
                        output_field=CharField(),
                        ),
                    entrega_ico=Case(
                        When(pedido__retira=True, then=Value("fab fa-pied-piper-alt ok")),
                        default=F('pedido__user__coagri__partilha__icone'),
                        output_field=CharField(),
                        )
        )
    locais_tb = coagris_tb.values(
                'entrega', 'entrega_ico', 'higieniza', 'nomeitem'
            ).order_by(
                'entrega', 'entrega_ico', 'higieniza', 'nomeitem'
            ).annotate(soma=Sum('qtde'))

    context={'ativa_tb': ativa_tb,
                'locais_tb': locais_tb,
                'coagris_tb': coagris_tb,
            }
    return render (request, template_name, context)