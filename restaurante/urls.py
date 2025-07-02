
from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_restaurante, name='landing_restaurante'),
    path('menu/', views.menu_completo, name='menu_completo'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('agregar-carrito/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('confirmar-pedido/', views.confirmar_pedido, name='confirmar_pedido'),
    path('mis-pedidos/', views.mis_pedidos, name='mis_pedidos'),
    path('pedido/<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),
    path('registro/',views.usuarios,name='registro'),
]
