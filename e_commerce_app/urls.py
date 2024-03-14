from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', index_page, name='home'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('add_to_cart/<int:pk>', add_to_cart, name='add_to_cart'),
    path('view_cart/', view_cart, name='view_cart'),
    path('remove_item_from_cart/<int:pk>', remove_item_from_cart, name='remove_item_from_cart'),

    path('display_shoe/<int:pk>', display_each_shoe, name='display_each_shoe'),
    path('checkout/', checkout, name='checkout'),
    path('order_confirmed/', order_confirmed, name='order_confirmed'),

    path('orders/', view_order, name='orders'),
    path('view_order/<int:order_id>', view_single_order, name='view_single_order'),

    path('all_shoes/', view_all_shoes_by_category, name='all_shoes_by_category'),
]
