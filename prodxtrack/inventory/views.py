from django.shortcuts import render,redirect, get_object_or_404
from .models import Inventory,Inbound,Outbound
from .forms import InventoryForm, InboundForm, OutboundForm
from django.contrib import messages


# Homepage
def index(request):
    # Calculate the total number of unique categories
    total_categories = Inventory.objects.values('category').distinct().count()
    
    # Manually calculate the total quantity in stock
    total_stock_quantity = 0
    for item in Inventory.objects.all():
        total_stock_quantity += item.quantity
    
    # Manually calculate the total quantity of inbound transactions
    total_inbound_quantity = 0
    for inbound in Inbound.objects.all():
        total_inbound_quantity += inbound.quantity
    
    # Manually calculate the total quantity of outbound transactions
    total_outbound_quantity = 0
    for outbound in Outbound.objects.all():
        total_outbound_quantity += outbound.quantity
    
    context = {
        'total_categories': total_categories,
        'total_stock_quantity': total_stock_quantity,
        'total_inbound_quantity': total_inbound_quantity,
        'total_outbound_quantity': total_outbound_quantity,
    }
    return render(request, 'inventory/index.html', context)

# CRUD inventory
def inventory_list(request):
    search_field = request.GET.get('search_field')  # Get the field to search by (e.g., 'category', 'sku', etc.)
    query = request.GET.get('q')  # Get the search term
    items = Inventory.objects.all()

    if query and search_field:
        if search_field == 'category':
            items = items.filter(category__icontains=query)
        elif search_field == 'sku':
            items = items.filter(sku__icontains=query)
        elif search_field == 'name':
            items = items.filter(name__icontains=query)
        elif search_field == 'location':
            items = items.filter(location__icontains=query)
        elif search_field == 'supplier':
            items = items.filter(supplier__icontains=query)
    
    context = {
        'items': items,
        'query': query,
        'search_field': search_field,
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
            inbound_record = form.save(commit=False)  # Create the Inbound object but don't save it yet
            # Update the inventory quantity
            inbound_record.product_sku.quantity += inbound_record.quantity
            inbound_record.product_sku.save()
            # Save the inbound record
            inbound_record.save()
            return redirect('view_inbound_history')
    else:
        form = InboundForm()
        
    context = {
        'form': form
    }
    return render(request, 'inventory/record_inbound.html', context)


def view_inbound_history(request):
    search_field = request.GET.get('search_field')  
    query = request.GET.get('q')  # Get the search term
    inbound_records = Inbound.objects.all().order_by('-date_received')

    if query and search_field:
        if search_field == 'product_name':
            inbound_records = inbound_records.filter(product_sku__name__icontains=query)
        elif search_field == 'supplier_name':
            inbound_records = inbound_records.filter(supplier_name__icontains=query)
        elif search_field == 'location':
            inbound_records = inbound_records.filter(location__icontains=query)
    
    context = {
        'inbound_records': inbound_records,
        'query': query,
        'search_field': search_field,
    }
    return render(request, 'inventory/inbound_history.html', context)

# OUTBOUND
def record_outbound(request):
    if request.method == 'POST':
        form =  OutboundForm(request.POST)
        if form.is_valid():
            outbound_record = form.save(commit=False)  # Create the Outbound object but don't save it yet
            if outbound_record.quantity > outbound_record.product_sku.quantity:
                messages.error(request, 'Error: Not enough inventory for this outbound operation.')
                return redirect('record_outbound')
            else:
                # Update the inventory quantity
                outbound_record.product_sku.quantity -= outbound_record.quantity
                outbound_record.product_sku.save()
                # Save the outbound record
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
    search_field = request.GET.get('search_field')  
    query = request.GET.get('q') 
    outbound_records = Outbound.objects.all().order_by('-date_shipped')

    if query and search_field:
        if search_field == 'product_name':
            outbound_records = outbound_records.filter(product_sku__name__icontains=query)
        elif search_field == 'destination':
            outbound_records = outbound_records.filter(destination__icontains=query)
        elif search_field == 'customer_name':
            outbound_records = outbound_records.filter(customer_name__icontains=query)
    
    context = {
        'outbound_records': outbound_records,
        'query': query,
        'search_field': search_field,
    }
    return render(request, 'inventory/outbound_history.html', context)