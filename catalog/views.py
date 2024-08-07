from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    TemplateView,
    CreateView,
    UpdateView,
    DeleteView,
)

from catalog.forms import ProductForm, VersionForm, ProductModeratorForm
from catalog.models import Product, Version, Category
from catalog.services import get_cached_categories, get_cached_products


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.owner = user
        product.save()
        return super().form_valid(form)


class ProductListView(ListView):
    model = Product
    extra_context = {"title": "Все продукты"}

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.groups.filter(name='moderator').exists() or user.is_superuser:
                return get_cached_products(is_published=False)
            else:
                return get_cached_products(is_published=True)
        else:
            return get_cached_products(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user_is_moderator'] = user.is_authenticated and (
                user.groups.filter(name='moderator').exists() or user.is_superuser)
        return context


class ProductDetailView(DetailView):
    model = Product


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse("catalog:view_product", args=[self.kwargs.get("pk")])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(
            Product, Version, form=VersionForm, extra=1
        )
        if self.request.method == "POST":
            context_data["formset"] = VersionFormset(
                self.request.POST, instance=self.object
            )
        else:
            context_data["formset"] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()["formset"]
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        if (
                user.has_perm("catalog.set_published_status")
                and user.has_perm("catalog.can_edit_description")
                and user.has_perm("catalog.can_edit_category")
        ):
            return ProductModeratorForm
        raise PermissionDenied


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:home")


class ContactsTemplateView(TemplateView):
    template_name = "catalog/contacts.html"


class CategoryListView(ListView):
    model = Category
    extra_context = {"title": "Категории продуктов"}

    def get_queryset(self):
        return get_cached_categories()


class CategoryProductsListView(ListView):
    model = Product
    template_name = "catalog/category_products.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.filter(category__name=self.kwargs["category"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(name=self.kwargs["category"])
        context['category'] = category
        return context
