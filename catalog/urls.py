from django.urls import path

from catalog import views

urlpatterns = [
    path('', views.home, name='home'),
]