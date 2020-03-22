from django.http import JsonResponse

from api.utils import create_tree, delete_tree, get_tree, get_graph, get_data
from rest_framework.decorators import api_view
import json


@api_view(['GET'])
def get_graph_api(request, id):
    response = get_graph(id)
    return JsonResponse(response)


@api_view(["GET"])
def get_tree_api(request):
    return JsonResponse(get_tree())


@api_view(["POST"])
def post(request):
    tree = [json.loads(request.body.decode())]
    response = create_tree(get_data(tree))
    return JsonResponse(response)


@api_view(["DELETE"])
def delete(request, id):
    response = delete_tree(id)
    return JsonResponse(response)
