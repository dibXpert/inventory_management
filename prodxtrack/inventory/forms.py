from django import forms
from .models import Inventory, Inbound, Outbound
from django.forms.widgets import DateInput
from django.contrib.auth.models import User


class CreateUserForm(forms.ModelForm):
    is_manager = forms.BooleanField(required=False, label='Is Manager?')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_manager', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

class EditUserForm(forms.ModelForm):
    is_manager = forms.BooleanField(required=False, label='Is Manager?')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'is_manager']

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory 
        fields = ['category', 'sku', 'name', 'location', 'quantity', 'supplier']

        
class InboundForm(forms.ModelForm):
    date_received = forms.DateField(widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Inbound
        fields = ['product_sku', 'quantity','location', 'reference', 'remarks','date_received','supplier_name']

       
class OutboundForm(forms.ModelForm):
    date_shipped = forms.DateField(widget=DateInput(attrs={'type': 'date'}))


    class Meta:
        model = Outbound
        fields = ['product_sku', 'quantity','destination', 'reference', 'remarks','date_shipped','customer_name']



    