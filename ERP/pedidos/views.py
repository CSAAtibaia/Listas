from django.shortcuts import render

# Create your views here.

def pedido_add(request):
    template_name='produto_form.html'
    return render(request, template_name)