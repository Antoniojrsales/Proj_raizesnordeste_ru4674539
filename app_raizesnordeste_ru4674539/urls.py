from django.urls import path
from .views import ProdutoListAPIView, PedidoListCreateAPIView

urlpatterns = [
    path('produtos/', ProdutoListAPIView.as_view(), name='produto-list'),
    path('pedidos/', PedidoListCreateAPIView.as_view(), name='pedido-list-create'),
]