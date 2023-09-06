from django.core.management import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        Product.objects.all().delete()
        Category.objects.all().delete()

        category_list = [
            {'id': 1, 'name': 'Смартфоны и гаджеты', 'description': 'Всегда в наличии последние модели'},
            {'id': 2, 'name': 'Электроника', 'description': 'На каждый товар гарантия 2 года'},
            {'id': 3, 'name': 'Мебель', 'description': 'Самая выгодная мебель от производителя'},
            {'id': 4, 'name': 'Техника для кухни', 'description': 'Самый большой выбор'}
        ]
        categories_for_create = []
        for category_item in category_list:
            categories_for_create.append(
                Category(**category_item)
            )

        Category.objects.bulk_create(categories_for_create)

        product_list = [
            {'name': 'iPhone', 'description': 'смартфон', 'category': Category.objects.get(id=1), 'price': 150000},
            {'name': 'Philips', 'description': 'пылесос', 'category': Category.objects.get(id=2), 'price': 50000},
            {'name': 'Ikea', 'description': 'стул', 'category': Category.objects.get(id=3), 'price': 5000},
            {'name': 'Siemens', 'description': 'плита', 'category': Category.objects.get(id=4), 'price': 70000},
        ]

        products_for_create = []
        for product_item in product_list:
            products_for_create.append(
                Product(**product_item)
            )

        Product.objects.bulk_create(products_for_create)
