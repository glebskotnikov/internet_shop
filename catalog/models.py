from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Категория')
    description = models.TextField(**NULLABLE, verbose_name='Описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    photo = models.ImageField(upload_to='products/', **NULLABLE, verbose_name='Фото')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.IntegerField(verbose_name='Цена за покупку')
    date_of_creation = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', **NULLABLE)
    date_last_modified = models.DateTimeField(verbose_name='Дата последнего изменения', **NULLABLE)
    is_published = models.BooleanField(default=False, verbose_name='Признак публикации')

    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Владелец', **NULLABLE)

    def __str__(self):
        return f'{self.name} ({self.category})'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ['name']
        permissions = [
            ('set_published_status', 'Can publish product'),
            ('can_edit_description', 'Can edit description'),
            ('can_edit_category', 'Can edit category')
        ]


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='versions', **NULLABLE)
    number_version = models.PositiveIntegerField(verbose_name='Номер версии')
    name = models.CharField(max_length=150, verbose_name='Название')
    current_version = models.BooleanField(verbose_name='признак текущей версии', default=False)

    def __str__(self):
        return f'{self.product.name} ({self.number_version})'

    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'
