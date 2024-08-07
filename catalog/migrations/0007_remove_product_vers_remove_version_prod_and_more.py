# Generated by Django 4.2.5 on 2023-09-29 03:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_rename_product_version_prod_product_vers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='vers',
        ),
        migrations.RemoveField(
            model_name='version',
            name='prod',
        ),
        migrations.AddField(
            model_name='version',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='versions', to='catalog.product'),
        ),
    ]
