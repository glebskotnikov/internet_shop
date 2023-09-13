from django.shortcuts import render
from django.views.generic import ListView
from catalog.models import Product


# class ProductListView(ListView):
#     model = Product
#     template_name = 'catalog/home.html'

def home(request):
    # print(Product.objects.all()[:5])
    context = {
        'objects_list': Product.objects.all(),
        'title': 'Каталог'
    }
    return render(request, 'catalog/home.html', context)


def product(request, pk):
    context = {
        'object': Product.objects.get(pk=pk)
    }
    return render(request, 'catalog/product.html', context)


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'{name} ({phone}): {message}')
    return render(request, 'catalog/contacts.html')
