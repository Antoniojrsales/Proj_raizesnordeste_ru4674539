from django.urls import path
from .views import ProdutoListAPIView, PedidoListCreateAPIView, PedidoPagamentoMockAPIView, HomeView    

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('produtos/', ProdutoListAPIView.as_view(), name='produto-list'),
    path('pedidos/', PedidoListCreateAPIView.as_view(), name='pedido-list-create'),
    path('pedidos/<int:pk>/pagar/', PedidoPagamentoMockAPIView.as_view(), name='pedido-pagar-mock'),
]