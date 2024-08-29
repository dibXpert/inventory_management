from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
   path('', views.index, name='index'), 
   
   #authentication
   path('login/', auth_views.LoginView.as_view(template_name='inventory/users/login.html'), name='login'),
   path('simple_logout/', views.custom_logout, name='custom_logout'),
   
   #user management
   path('create_user/', views.create_user, name='create_user'),
   path('edit_user/<int:pk>/', views.edit_user, name='edit_user'),
   path('delete_user/<int:pk>/', views.delete_user, name='delete_user'),
   path('user_list/', views.user_list, name='user_list'),
   
   #crud inventory
   path('inventory/', views.inventory_list, name='inventory_list'),
   path('add/', views.add_inventory, name='add_inventory'),
   path('edit/<int:pk>/', views.edit_inventory, name='edit_inventory'),
   path('delete/<int:pk>/', views.delete_inventory, name='delete_inventory'),
   
   #inbound
   path('inbound/',views.record_inbound, name='record_inbound'),
   path('inbound/history/', views.view_inbound_history, name='view_inbound_history'),
   path('inbound/edit/<int:pk>/', views.edit_inbound, name='edit_inbound'),
   path('inbound/delete/<int:pk>/', views.delete_inbound, name='delete_inbound'),
   
   #outbound
   path('outbound/', views.record_outbound, name='record_outbound'), 
   path('outbound/history/', views.view_outbound_history, name='view_outbound_history'),
   path('outbound/edit/<int:pk>/', views.edit_outbound, name='edit_outbound'),
   path('outbound/delete/<int:pk>/', views.delete_outbound, name='delete_outbound'),
]