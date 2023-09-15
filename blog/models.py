from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='заголовок')
    slug = models.CharField(max_length=100, verbose_name='slug')
    content = models.TextField(verbose_name='содержимое')
    image = models.ImageField(upload_to='blog/', verbose_name='изображение', **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    is_published = models.BooleanField(default=True, verbose_name='признак публикации')
    views_count = models.IntegerField(default=0, verbose_name='количество просмотров')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'
