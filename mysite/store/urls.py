from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.chekout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    # path('contacts/', views.contacts, name="contacts"),
    path('about/', views.about, name="about"),
    path('categories/', views.category_list, name='categories'),
    path('categories/<int:category_id>', views.get_store_by_categories, name='get_store_by_cat')
]
