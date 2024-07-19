from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify

from blog.forms import BlogForm
from blog.models import Blog


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        if form.is_valid():
            blog = form.save()
            user = self.request.user
            blog.owner = user
            blog.slug = slugify(blog.title)
            blog.save()

        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Blog
    form_class = BlogForm

    def form_valid(self, form):
        if form.is_valid():
            new = form.save()
            new.slug = slugify(new.title)
            new.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:view', args=[self.kwargs.get('slug')])

    def test_func(self):
        obj = self.get_object()
        return self.request.user.groups.filter(name='content-manager').exists() or \
            self.request.user.is_superuser or \
            obj.owner == self.request.user


class BlogListView(ListView):
    model = Blog
    extra_context = {"title": "Блог"}

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.groups.filter(name='content-manager').exists() or user.is_superuser:
                return Blog.objects.all()
            else:
                return Blog.objects.filter(is_published=True)
        else:
            return Blog.objects.filter(is_published=True)


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user_is_manager'] = user.is_authenticated and (
                user.groups.filter(name='content-manager').exists() or user.is_superuser)
        return context


class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:list')

    def test_func(self):
        obj = self.get_object()
        return self.request.user.groups.filter(name='content-manager').exists() or \
            self.request.user.is_superuser or \
            obj.owner == self.request.user


def toggle_activity(request, slug):
    blog_item = get_object_or_404(Blog, slug=slug)
    if blog_item.is_published:
        blog_item.is_published = False
    else:
        blog_item.is_published = True

    blog_item.save()

    return redirect('blog:view', slug=blog_item.slug)
