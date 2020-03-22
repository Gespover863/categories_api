from api.models import Categories
from django.db.utils import IntegrityError
from serializations.graph_serialization import graph_serialization
from serializations.tree_serialization import tree_serialization


def get_data(tree, parent=None):
    data = {
        "tree": tree,
        "parent": parent
    }
    return data


def get_graph(id):
    category = Categories.objects.filter(pk=id)
    if not category:
        return {
            "success": False,
            "result": [],
            "error": f'Идентификатор {id} не существует в базе.'
        }
    return graph_serialization(category[0])


def get_tree():
    trees = Categories.objects.filter(parent=None)
    result = []
    for category in trees:
        result.append(tree_serialization(category))
    response = {
        "success": True,
        "result": result,
        "error": None
    }
    return response


def create_tree(data):
    tree = data['tree']
    for graph in tree:
        category = Categories()
        category.name = graph['name']
        if data['parent'] is not None:
            category.parent = Categories.objects.get(id=data['parent'])
        try:
            category.save()
        except IntegrityError:
            return {
                "success": False,
                "result": [],
                "error": f'Категория с именем "{graph["name"]}" уже существует.'
            }

        if 'children' in graph and graph['children'] != []:
            children_data = get_data(graph['children'], category.id)
            response = create_tree(children_data)

            if type(response) == dict:
                if category.parent is None:
                    delete_tree(category.id)
                return response

            if category.parent is None:
                response = {
                    "success": True,
                    "result": tree_serialization(category),
                    "error": None
                }
                return response


def delete_tree(id):
    if not Categories.objects.filter(pk=id):
        return {
            "success": False,
            "result": [],
            "error": f'Идентификатор {id} не существует в базе.'
        }

    children = Categories.objects.raw(f'''
        WITH RECURSIVE graphs AS (
            SELECT id, parent_id, name
            FROM api_categories
            WHERE parent_id = {id}
            UNION
            SELECT api_categories.id, api_categories.parent_id, api_categories.name
            FROM api_categories
               JOIN graphs ON api_categories.parent_id = graphs.id
        )
        SELECT * FROM graphs;
    ''')

    for graph in children:
        Categories.objects.filter(pk=graph.id).delete()
    Categories.objects.filter(pk=id).delete()

    return {
        "success": True,
        "result": [],
        "error": None
    }
