from django.db import transaction

from .models import Module


def delete_item_and_refresh_order(module: Module, object):
    with transaction.atomic():
        object.delete()
        items = type(object).objects.filter(module=module).order_by("order")
        for index, item in enumerate(items, start=1):
            if item.order != index:
                item.order = index
                item.save()
