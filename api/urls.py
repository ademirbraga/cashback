# coding=utf8
from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

router.register(r'revendedor', views.RevendedorViewSet)
router.register(r'pedido', views.PedidoViewSet)
router.register(r'cashback-revendedor', views.CashBackRevendedorViewSet)
router.register(r'white-list', views.WhiteListPedidoViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]