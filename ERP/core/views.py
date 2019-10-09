from django.shortcuts import render
from datetime import datetime
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, ListView
from .models import Item as Produto
from .forms import ItemForm as ProdutoForm

# Create your views here.

def index(request):
    return render(request, 'index.html')

def produto_list(request):
    template_name = 'produto_list.html'
    objects = Produto.objects.all()
    search = request.GET.get('search')
    if search:
        objects = objects.filter(produto__icontains=search)
    context = {'object_list': objects}
    return render(request, template_name, context)


class ProdutoList(ListView):
    model = Produto
    template_name = 'produto_list.html'
    paginate_by = 10


def produto_detail(request, pk):
    template_name = 'produto_detail.html'
    obj = Produto.objects.get(pk=pk)
    context = {'object': obj}
    return render(request, template_name, context)


def produto_add(request):
    form = ProdutoForm(request.POST or None)
    template_name = 'produto_form2.html'

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('produto:produto_list'))

    context = {'form': form}
    return render(request, template_name, context)


class ProdutoCreate(CreateView):
    model = Produto
    template_name = 'produto_form.html'
    form_class = ProdutoForm


class ProdutoUpdate(UpdateView):
    model = Produto
    template_name = 'produto_form.html'
    form_class = ProdutoForm


def produto_json(request, pk):
    ''' Retorna o produto, id e estoque. '''
    produto = Produto.objects.filter(pk=pk)
    data = [item.to_dict_json() for item in produto]
    return JsonResponse({'data': data})


def save_data(data):
    '''
    Salva os dados no banco.
    '''
    aux = []
    for item in data:
        produto = item.get('produto')
        estoque = item.get('estoque')
        obj = Produto(
            produto=produto,
            estoque=estoque,
        )
        aux.append(obj)
    Produto.objects.bulk_create(aux)