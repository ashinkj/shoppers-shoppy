from django.urls import path
from . import views

urlpatterns = [
    
    path("",views.store,name="store-page"),
    path("addcart/",views.cart,name="cart-page"),
    path("checkout/",views.checkout,name="checkout-page"),
    path("update_item/",views.updateItem,name="update-item"),
    path("process_order/",views.processOrder,name="process-Order"),

]