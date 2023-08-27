from django.urls import path
from . import views

urlpatterns = [
    path('cycle/<int:c_id>/',views.productPage,name="productPage"),
    path('cart/',views.cartPage,name="cartPage"),
    path('order/',views.orderPage,name='orderPage'),
    path('return/order/<int:pk>',views.returnorderPage,name='returnorderPage')
]