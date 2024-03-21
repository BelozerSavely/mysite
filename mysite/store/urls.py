from django.urls import path
from . import views

urlpatterns = [
    path('', views.Store, name="store"),
    path('cart/', views.Cart, name="cart"),
    path('checkout/', views.Chekout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('contacts/', views.contacts, name="contacts"),
    path('about/', views.about, name="about")

]
