from django.urls import path
from . import views

urlpatterns = [
   path('', views.inventory_list, name='inventory_list'),
   path('add/', views.add_inventory, name='add-inventory'),
   path('inbound/',views.record_inbound, name='record_inbound'),
   path('outbound/', views.record_outbound, name='record_outbound'), 
]