# Generated by Django 4.2.4 on 2023-09-05 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_alter_category_options_alter_category_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='created_at',
            field=models.DateField(blank=True, null=True, verbose_name='Дата создания'),
        ),
    ]