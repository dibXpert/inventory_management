from django.urls import path
from . import views

urlpatterns = [
   path('', views.index, name='index'), 
   path('inventory/', views.inventory_list, name='inventory_list'),
   #crud inventory
   path('add/', views.add_inventory, name='add_inventory'),
   path('edit/<int:pk>/', views.edit_inventory, name='edit_inventory'),
   path('delete/<int:pk>/', views.delete_inventory, name='delete_inventory'),
   
   
   #inbound
   path('inbound/',views.record_inbound, name='record_inbound'),
   #outbound
   path('outbound/', views.record_outbound, name='record_outbound'), 
]