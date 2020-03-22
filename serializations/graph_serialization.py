from api.models import Categories
from django.db.models import Q


def data(category):
    category = {
        "id": category.id,
        "name": category.name
    }
    return category


def graph_serialization(category):
    result = {
        "id": category.id,
        "name": category.name,
        "parents": [],
        "children": [],
        "sublings": [],
    }

    parents = Categories.objects.raw(f'''
                WITH RECURSIVE graphs AS (
                    SELECT id, parent_id, name
                    FROM api_categories
                    WHERE id = {category.id}
                    UNION
                    SELECT ac.id, ac.parent_id, ac.name
                    FROM api_categories ac, graphs
                    WHERE ac.id = graphs.parent_id
                )
                SELECT * FROM graphs WHERE id != {category.id};
            ''')
    children = Categories.objects.filter(parent=category.id)
    sublings = Categories.objects.filter(~Q(pk=category.id), parent=category.parent)

    for category in parents:
        result['parents'].append(data(category))

    for category in children:
        result['children'].append(data(category))

    for category in sublings:
        result['sublings'].append(data(category))

    response = {
        "success": True,
        "result": result,
        "error": None
    }
    return response
