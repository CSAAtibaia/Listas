from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max, Sum
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, resolve_url, redirect
from django.views.generic import ListView, DetailView #, UpdateView
from ERP.core.models import CoAgri, Item #, Situacao
from .models import Estoque, Lista as EstoqueEntrada, Pedido as EstoqueSaida, EstoqueItens
from .forms import EstoqueForm, EstoqueItensForm, PedidoItemForm
from django.db import connection
from django.contrib import messages
from django.contrib.auth.models import User
from ERP.estoque.email import email_abertura, email_fechamento, email_pedido
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


def recalcular_estoque():
    entradas = EstoqueItens.objects.filter(estoque__movimento='e', estoque__aberto=True)
    entradas = entradas.values('produto').annotate(entrada=Sum('quantidade'))
    saidas = EstoqueItens.objects.filter(estoque__movimento='s', estoque__aberto=True)
    saidas = saidas.values('produto').annotate(saida=Sum('quantidade'))
    for produto in entradas:
        item = Item.objects.get(pk=produto['produto'])
        try:
            saida_dict = saidas.get(produto=produto['produto'])
            saida = saida_dict['saida']
        except ObjectDoesNotExist:
            saida = 0

        entrada = produto['entrada']
        item.saldo = entrada - saida
        item.save()


@login_required(login_url='login/')
def finalizar(request):
    cursor1 = connection.cursor()
    cursor1.execute("update estoque_estoque set aberto = FALSE")
    email_fechamento()
    messages.success(request, 'Finalizado com sucesso')
    return redirect('estoque:controle')


@login_required(login_url='login/')
def reiniciar(request):
    cursor1 = connection.cursor()
    cursor1.execute("update core_item as c set c.saldo = 0")
    cursor1.execute("update estoque_estoque set aberto = FALSE")
    messages.success(request, 'Encerrado com sucesso')
    return redirect('estoque:controle')


@login_required(login_url='login/')
def pedido_enviar(request, pk):
    listinha = EstoqueItens.objects.filter(estoque=pk)
    mensagem = 'Pedido:\n\t\t'
    for ei in listinha:
        mensagem = mensagem + '%s - %s;\n\t\t' % (ei.produto, ei.quantidade)
    mensagem = mensagem + 'Confirmado.'
    messages.success(request, mensagem)
    email_pedido(request.user, mensagem)
    return redirect('core:index')


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
            recalcular_estoque()
            email_abertura()
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
    objects = Estoque.objects.filter(aberto=true,
                                     movimento='s')
    context = {
        'object_list': objects,
        'titulo': 'Pedido',
        'url_add': 'estoque:pedido_update'
    }
    return render(request, template_name, context)


def estoque_saida_detail(request, pk):
    template_name = 'estoque_detail.html'
    obj = EstoqueSaida.objects.get(pk=pk)
    context = {
        'object': obj,
        'url_list': 'estoque:estoque_saida_list'
    }
    return render(request, template_name, context)


@login_required(login_url='login/')
def pedido_edit(request):
    coagri = CoAgri.objects.get(user=request.user)
    if coagri.status == 'ATIVO' or coagri.status == 'AVISO':
        q = Estoque.objects.filter(aberto=True, movimento='e').aggregate(fim=Max('finaliza'))
        finaliza = q['fim']
        if finaliza is not None:
            try:
                pedido = Estoque.objects.get(aberto=True, movimento='s', usuario=request.user)
            except Estoque.DoesNotExist:
                pedido = Estoque(
                            aberto=True,
                            movimento='s',
                            finaliza=finaliza,
                            usuario=request.user
                                )
                pedido.save()
        else:
            messages.warning(request, 'Sem lista aberta. Por favor aguarde.')
            return redirect('core:index')
    else:
        messages.error(request, 'CoAgricultor sem permissão para Pedidos')
        return redirect('core:index')

    pedido_itens_formset = inlineformset_factory(
                                Estoque,
                                EstoqueItens,
                                form=PedidoItemForm,
                                extra=1,
                                can_delete=False)

    itens = pedido_itens_formset(request.POST or None, instance=pedido, prefix='item')
    if request.method == 'POST':
        if itens.is_valid():
            itens.save()
            recalcular_estoque()
            messages.success(request, 'Item atualizado com sucesso')
            return HttpResponseRedirect(resolve_url('estoque:pedido_update'))
        messages.error(request, 'Pedido não Salvo')
        return HttpResponseRedirect(resolve_url('estoque:pedido_update'))

    return render(request, 'pedido_update.html',
        {"itens": itens, "pedido": pedido, "coagri": coagri})

@login_required(login_url='login/')
def controle(request):
    template_name = 'controle.html'
    return render(request, template_name, {"titulo":'Controle de Fechamento'})


def sem_pedido(request):
    template_name = 'sem_pedido.html'
    objects = User.objects.exclude(
        estoque__aberto=True,
        estoque__movimento='s'
        ).order_by('first_name', 'username')
    context = {
        'object_list': objects,
        'titulo': 'Sem Pedido',
    }
    return render(request, template_name, context)
