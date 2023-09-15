from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView

from catalog.models import Product


class ProductListView(ListView):
    model = Product
    extra_context = {
        'title': 'Каталог'
    }


class ProductDetailView(DetailView):
    model = Product


class ContactsTemplateView(TemplateView):
    template_name = 'catalog/contacts.html'

# def contacts(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         phone = request.POST.get('phone')
#         message = request.POST.get('message')
#         print(f'{name} ({phone}): {message}')
#     return render(request, 'catalog/contacts.html')
