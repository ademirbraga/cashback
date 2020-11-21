# coding=utf8
"""cashbackconfig URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from revendedor.views import RevendedorViewSet
from pedido.views import PedidoViewSet
from whitelistpedido.views import WhiteListPedidoViewSet
from cashbackrevendedor.views import CashBackRevendedorViewSet

router = routers.DefaultRouter()

router.register(r'revendedor', RevendedorViewSet)
router.register(r'cadastrar-pedido', PedidoViewSet)
router.register(r'cashbackconfig-revendedor', CashBackRevendedorViewSet)
router.register(r'white-list', WhiteListPedidoViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('listar-pedidos', PedidoViewSet.as_view({'get': 'listar_pedidos'})),
    url(r'cashback-acumulado/(?P<cpf>[0-9]{11})$', CashBackRevendedorViewSet.as_view({'get': 'cashback_acumulado'})),
    url(r'^login/', obtain_jwt_token),
    url(r'^refresh-token/', refresh_jwt_token),
]