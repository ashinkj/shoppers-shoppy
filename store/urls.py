from django.urls import path
from . import views
from .views import PostDetailView

urlpatterns = [
    
    path("",views.store,name="store-page"),
    path('product/<int:pk>/', PostDetailView.as_view(), name='product-detail'),
    path("search_category/",views.search_category,name="search-category"),
    path("addcart/",views.cart,name="cart-page"),
    path("checkout/",views.checkout,name="checkout-page"),
    path("update_item/",views.updateItem,name="update-item"),
    path("process_order/",views.processOrder,name="process-order"),


]