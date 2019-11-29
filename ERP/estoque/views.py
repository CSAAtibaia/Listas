from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory, modelformset_factory
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render, resolve_url
from django.views.generic import ListView, DetailView #, UpdateView
from ERP.core.models import Item as Produto, CoAgri
from .models import Estoque, Lista as EstoqueEntrada, Pedido as EstoqueSaida, EstoqueItens
from .forms import EstoqueForm, EstoqueItensForm, PedidoItemForm
#from django.template                import RequestContext
from django.db import connection
import logging

logger = logging.getLogger(__name__)

def estoque_entrada_list(request):
    template_name = 'estoque_list.html'
    objects = EstoqueEntrada.objects.all()
    context = {
        'object_list': objects,
        'titulo': 'Lista',
        'url_add': 'estoque:estoque_entrada_add',
    }
    return render(request, template_name, context)


class EstoqueEntradaList(ListView):
    model = EstoqueEntrada
    template_name = 'estoque_list.html'

    def get_context_data(self, **kwargs):
        context = super(EstoqueEntradaList, self).get_context_data(**kwargs)
        context['titulo'] = 'Lista'
        context['url_add'] = 'estoque:estoque_entrada_add'
        return context


def estoque_entrada_detail(request, pk):
    template_name = 'estoque_detail.html'
    obj = EstoqueEntrada.objects.get(pk=pk)
    context = {
        'object': obj,
        'url_list': 'estoque:estoque_entrada_list'
    }
    return render(request, template_name, context)


class EstoqueDetail(DetailView):
    model = Estoque
    template_name = 'estoque_detail.html'


def recalcular_estoque:
    cursor1 = connection.cursor()
    cursor1.execute("update core_item as c " + 
                    "inner join ( " + 
                    "select a.produto_id, sum(a.qtde) as total " + 
                    "from ( " + 
                    "select i.produto_id, " + 
                    "(CASE WHEN e.movimento = 'e' THEN i.quantidade ELSE i.quantidade * -1 END) as qtde  " + 
                    "from estoque_estoqueitens i inner join estoque_estoque e on (i.estoque_id = e.id) " + 
                    "where e.aberto = TRUE) a " + 
                    "group by a.produto_id) as g " + 
                    "on c.id = g.produto_id " + 
                    "set c.saldo = g.total")


def finalizar:
    cursor1 = connection.cursor()
    cursor1.execute("update core_item as c set c.saldo = 0")
    cursor1.execute("update estoque_estoque set aberto = FALSE")


def estoque_add(request, template_name, movimento, url):
    estoque_form = Estoque()
    item_estoque_formset = inlineformset_factory(
        Estoque,
        EstoqueItens,
        form=EstoqueItensForm,
        extra=0,
        can_delete=False,
        min_num=1,
        validate_min=True,
    )
    if request.method == 'POST':
        form = EstoqueForm(request.POST, instance=estoque_form, prefix='main')
        formset = item_estoque_formset(
            request.POST,
            instance=estoque_form,
            prefix='estoque'
        )
        if form.is_valid() and formset.is_valid():
            form = form.save(commit=False)
            form.usuario = request.user
            form.movimento = movimento
            form.save()
            formset.save()
            recalcular_estoque
            return {'pk': form.pk}
    else:
        form = EstoqueForm(instance=estoque_form, prefix='main')
        formset = item_estoque_formset(instance=estoque_form, prefix='estoque')
    context = {'form': form, 'formset': formset}
    return context


@login_required(login_url='login/')
def estoque_entrada_add(request):
    template_name = 'estoque_entrada_form.html'
    movimento = 'e'
    url = 'estoque:estoque_detail'
    context = estoque_add(request, template_name, movimento, url)
    if context.get('pk'):
        return HttpResponseRedirect(resolve_url(url, context.get('pk')))
    return render(request, template_name, context)


def estoque_saida_list(request):
    template_name = 'estoque_list.html'
    objects = EstoqueSaida.objects.all()
    context = {
        'object_list': objects,
        'titulo': 'Pedido',
        'url_add': 'estoque:estoque_saida_add'
    }
    return render(request, template_name, context)


class EstoqueSaidaList(ListView):
    model = EstoqueSaida
    template_name = 'estoque_list.html'

    def get_context_data(self, **kwargs):
        context = super(EstoqueSaidaList, self).get_context_data(**kwargs)
        context['titulo'] = 'Pedido'
        context['url_add'] = 'estoque:estoque_saida_add'
        return context


def estoque_saida_detail(request, pk):
    template_name = 'estoque_detail.html'
    obj = EstoqueSaida.objects.get(pk=pk)
    context = {
        'object': obj,
        'url_list': 'estoque:estoque_saida_list'
    }
    return render(request, template_name, context)


@login_required(login_url='login/')
def estoque_saida_add(request):
    template_name = 'estoque_saida_form.html'
    movimento = 's'
    url = 'estoque:estoque_detail'
    context = estoque_add(request, template_name, movimento, url)
    if context.get('pk'):
        return HttpResponseRedirect(resolve_url(url, context.get('pk')))
    return render(request, template_name, context)


def pedido_edit(request):
    cursor1 = connection.cursor()
    #insere preemptivo pedido
    cursor1.execute("insert into estoque_estoque (created, modified, movimento, usuario_id, finaliza, aberto) " +
                    "select NOW(), null, 's', c.user_id, null, True from core_coagri c " +
                    "where c.status like 'A%%' and c.user_id not in (select p.usuario_id from estoque_estoque p " +
                    "where p.aberto = True and p.movimento = 's')")

    pedido = Estoque.objects.get(aberto=True, usuario=request.user, movimento='s')
    return pedido_manager(request, pedido)


@login_required(login_url='login/')
def pedido_manager(request, pedido):
    pedido_itens_formset = modelformset_factory(
                                EstoqueItens,
                                form=PedidoItemForm,
                                extra=0,
                                fields=('produto', 'quantidade', 'saldo',),
                                can_delete=False)
    pedidopk = pedido.pk
    #pedidoitens = EstoqueItens.objects.all
    #logger.error(pedidoitens)
    itens = pedido_itens_formset(request.POST or None, queryset=(EstoqueItens.objects.filter(estoque_id=pedidopk)), prefix='item')
    coagri = CoAgri.objects.get(user=request.user)
    #logger.error(formset)
    if itens.is_valid():
        itens.save()
        return HttpResponseRedirect(reverse_lazy('/estoque/pedido/'))

    return render(request, 'pedido_update.html',
        {"itens": itens, "pedido": pedido, "coagri": coagri})