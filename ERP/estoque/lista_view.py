from django.shortcuts import render
from ERP.estoque.models import Estoque, EstoqueItens
from ERP.core.models import Item
from django.db.models import Sum, F, CharField, IntegerField, Case, When, Value #, Q
from django.db.models.functions import Coalesce, Cast
# Create your views here.


def lista_itens(request):
    template_name = 'lista_ativa.html'

    ativa_tb = Estoque.objects.filter(movimento='s', aberto=True)

    pedidos_item_tb = EstoqueItens.objects.filter(estoque__in = ativa_tb, quantidade__gt = 0)

    itens = Item.objects.filter(
            estoqueitens__gt=0, estoqueitens__estoque__aberto=True
        ).values(
            'produto', 'saldo',
            nome_forn=F('fornecedor__nome')
        ).order_by(
            'fornecedor__nome', 'produto'
        ).distinct().annotate(
            qtde=Sum(
                Case(
                    When(estoqueitens__estoque__movimento='s', then=F('estoqueitens__quantidade')),
                    default=0,
                    output_field=IntegerField(),
                    )))

    coagris_tb = pedidos_item_tb.values(
            higieniza=F('estoque__usuario__coagri__higieniza'),
            coagri=Coalesce(
                Cast('estoque__usuario__coagri__apelido', CharField()),
                Cast('estoque__usuario__email', CharField()),
                Cast('estoque__usuario__username', CharField())
                ),
            nomeitem=F('produto__produto'),
            total=F('quantidade')
        ).annotate(entrega=Case(
                        When(estoque__usuario__coagri__retira=True, then=Value("Retira")),
                        default=F('estoque__usuario__coagri__partilha__partilha'),
                        output_field=CharField(),
                        ),
                    entrega_ico=Case(
                        When(estoque__usuario__coagri__retira=True, then=Value("fab fa-pied-piper-alt ok")),
                        default=F('estoque__usuario__coagri__partilha__icone'),
                        output_field=CharField(),
                        )
        )
    locais_tb = coagris_tb.values(
                'entrega', 'entrega_ico', 'higieniza', 'nomeitem'
            ).order_by(
                'entrega', 'entrega_ico', 'higieniza', 'nomeitem'
            ).annotate(soma=Sum('quantidade'))

    context = {'ativa_tb': ativa_tb,
                'locais_tb': locais_tb,
                'coagris_tb': coagris_tb,
                'itens': itens,}
    return render(request, template_name, context)
