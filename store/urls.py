from django.urls import path
from . import views

urlpatterns = [
    
    path("",views.store,name="store-page"),
    path("addcart/",views.cart,name="cart-page"),
    path("checkout/",views.checkout,name="checkout-page"),

]