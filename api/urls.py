# coding=utf8
from django.urls import include, path
from django.conf.urls import url
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

router.register(r'cadastrar-revendedor', views.RevendedorViewSet)
router.register(r'cadastrar-pedido', views.PedidoViewSet)
router.register(r'cashback-revendedor', views.CashBackRevendedorViewSet)
router.register(r'white-list', views.WhiteListPedidoViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('listar-pedidos', views.PedidoViewSet.as_view({'get': 'list'})),
    url(r'cashback-acumulado/(?P<cpf>[0-9]{11})$', views.CashBackRevendedorViewSet.as_view({'get': 'cashback_acumulado'})),
]