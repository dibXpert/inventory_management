from django import forms
from .models import Inventory, Inbound, Outbound

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory 
        fields = ['category', 'sku', 'name', 'location', 'quantity', 'supplier']

        
class InboundForm(forms.ModelForm):
    class Meta:
        model = Inbound
        fields = ['product_sku', 'quantity','location', 'reference', 'remarks','date_received','supplier_name']

       
class OutboundForm(forms.ModelForm):
    class Meta:
        model = Outbound
        fields = ['product_sku', 'quantity','destination', 'reference', 'remarks','date_shipped','customer_name']



    