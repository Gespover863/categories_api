from django.urls import path
from api.views import get_graph_api, get_tree_api, post, delete

urlpatterns = [
    path('get_graph/<int:id>', get_graph_api),
    path('get_tree/', get_tree_api),
    path('create_tree/', post),
    path('delete_tree/<int:id>', delete)
]
