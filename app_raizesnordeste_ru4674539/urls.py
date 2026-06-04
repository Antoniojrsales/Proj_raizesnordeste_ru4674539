from django.urls import path
from .views import ProdutoListAPIView, PedidoListCreateAPIView, PedidoPagamentoMockAPIView, HomeView, TotemView, CriarPedidoView, PagamentoView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('produtos/', ProdutoListAPIView.as_view(), name='produto-list'),
    path('pedidos/', PedidoListCreateAPIView.as_view(), name='pedido-list-create'),
    path('pedidos/criar/', CriarPedidoView.as_view(), name='pedido-criar'),
    path('totem/', TotemView.as_view(), name='totem'),
    path('totem/criar-pedido/', CriarPedidoView.as_view(), name='criar-pedido'),
    path('totem/pagamento/<int:pedido_id>/', PagamentoView.as_view(), name='pagamento'),
]