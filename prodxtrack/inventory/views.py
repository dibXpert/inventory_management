from django.shortcuts import render,redirect
from .models import Inventory,Inbound,Outbound
from .forms import InventoryForm, InboundForm, OutboundForm
# Create your views here.

def inventory_list(request):
    inventory_items = Inventory.objects.all()
    context = {
        'inventory_items':inventory_items,
    }
    return render(request, 'inventory/inv_list.html', context)

def add_inventory(request):
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory_list')
    else:
        form = InventoryForm()
        
    context = {
        'form': form
    }
    return render(request, 'inventory/add_inv.html',context)

# INBOUND
def record_inbound(request):
    if request.method == 'POST':
        form = InboundForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory_list')
    else:
        form = InboundForm()
        
    context = {
        'form': form
    }
    return render(request, 'inventory/record_inbound.html', context)

# OUTBOUND
def record_outbound(request):
    if request.method == 'POST':
        form =  OutboundForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory_list')
    else:
        form = OutboundForm()
        
    context = {
        'form': form
    }
    return render(request, 'inventory/record_outbound.html', context)

