from django.db import models

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
    vers = models.ForeignKey('Version', on_delete=models.DO_NOTHING, verbose_name='Версия', **NULLABLE)

    def __str__(self):
        return f'{self.name} ({self.category})'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'


class Version(models.Model):
    prod = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    number_version = models.PositiveIntegerField(verbose_name='Номер версии')
    name = models.CharField(max_length=150, verbose_name='Название')
    current_version = models.BooleanField(verbose_name='признак текущей версии', default=False)

    def __str__(self):
        return f'{self.prod.name} ({self.number_version})'

    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'