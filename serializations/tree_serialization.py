from api.models import Categories
from django.db.models import Q


def data(category):
    category = {
        "id": category.id,
        "name": category.name
    }
    return category


def tree_serialization(category):
    result = {
        "id": category.id,
        "name": category.name,
        "children": [],
    }

    children = Categories.objects.filter(parent=category.id)

    if not children:
        result['children'].append(data(category))
        return result

    for graph in children:
        result['children'].append(tree_serialization(graph))

    return result
