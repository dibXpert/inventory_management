from django.shortcuts import render,redirect, get_object_or_404
from .models import Inventory,Inbound,Outbound
from .forms import InventoryForm, InboundForm, OutboundForm
from django.contrib import messages


# Homepage
def index(request):
    return render(request, 'inventory/index.html')

# CRUD inventory
def inventory_list(request):
    items = Inventory.objects.all()
    context = {
        'items':items,
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

def edit_inventory(request, pk):
    item = get_object_or_404(Inventory, pk=pk)
    if request.method == 'POST':
        form = InventoryForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('inventory_list')
    else:
        form = InventoryForm(instance=item)
    
    context = {
        'form': form,
        'item':item,
    }
    return render(request, 'inventory/edit_inv.html', context)
        
def delete_inventory(request,pk):
    item = get_object_or_404(Inventory, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('inventory_list')
    
    context = {
        'item': item
        
    }
    return render(request, 'inventory/delete_inv.html', context)

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

def view_inbound_history(request):
    inbound_records = Inbound.objects.all().order_by('-date_received')
    context = {
        'inbound_records': inbound_records,
    }
    return render(request, 'inventory/inbound_history.html', context)


# OUTBOUND
def record_outbound(request):
    if request.method == 'POST':
        form =  OutboundForm(request.POST)
        if form.is_valid():
            outbound_record = form.save(commit=False)
            if outbound_record.quantity > outbound_record.product_sku.quantity:
                messages.error(request, 'Error: Not enough inventory for this outbound operation.')
                return redirect('record_outbound')
            else:
                outbound_record.save()
                messages.success(request, 'Outbound record added successfully.')
                return redirect('inventory_list')
    else:
        form = OutboundForm()
        
    context = {
        'form': form
    }
    return render(request, 'inventory/record_outbound.html', context)

def view_outbound_history(request):
    outbound_records = Outbound.objects.all().order_by('-date_shipped')
    context = {
        'outbound_records': outbound_records,
    }
    return render(request, 'inventory/outbound_history.html', context)
