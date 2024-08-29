from django.shortcuts import render,redirect, get_object_or_404
from .models import Inventory,Inbound,Outbound
from .forms import InventoryForm, InboundForm, OutboundForm
from django.contrib import messages

from django.contrib.auth.decorators import login_required, user_passes_test
from .models import UserProfile
from .forms import CreateUserForm,EditUserForm
from django.contrib.auth.models import User

from django.contrib.auth import logout
def custom_logout(request):
    logout(request)
    return redirect('login')

#user management

def is_manager(user):
    return user.userprofile.is_manager


@login_required
def create_user(request):
    if request.method == 'POST':
        user_form = CreateUserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])  # Set password correctly
            user.save()

            # Create a UserProfile for the new user
            is_manager = user_form.cleaned_data['is_manager']
            UserProfile.objects.create(user=user, is_manager=is_manager)
            return redirect('user_list')
    else:
        user_form = CreateUserForm()

    context = {
        'user_form': user_form,
    }
    return render(request, 'inventory/users/create_user.html', context)

@login_required
@user_passes_test(is_manager)
def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    # Retrieve the associated UserProfile instance
    user_profile = get_object_or_404(UserProfile, user=user)

    if request.method == 'POST':
        user_form = EditUserForm(request.POST, instance=user)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            
            # Update the UserProfile's is_manager field
            user_profile.is_manager = user_form.cleaned_data['is_manager']
            user_profile.save()

            user.save()
            return redirect('user_list')
    else:
        # Initialize the form with existing data, including the is_manager field
        initial_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_manager': user_profile.is_manager
        }
        user_form = EditUserForm(instance=user, initial=initial_data)

    context = {
        'user_form': user_form,
        'user': user,
    }
    return render(request, 'inventory/users/edit_user.html', context)

@login_required
@user_passes_test(is_manager)
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')

    context = {
        'user': user,
    }
    return render(request, 'inventory/users/delete_user.html', context)


@login_required
def user_list(request):
    users = User.objects.all()
    context = {
        'users': users,
    }
    return render(request, 'inventory/users/user_list.html', context)



# Homepage
@login_required
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
@login_required
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

@login_required
@user_passes_test(is_manager)
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

@login_required
@user_passes_test(is_manager)
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

@login_required
@user_passes_test(is_manager)       
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
@login_required
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
            messages.success(request, 'Inbound record added successfully.')
            return redirect('view_inbound_history')
    else:
        form = InboundForm()
        
    context = {
        'form': form
    }
    return render(request, 'inventory/record_inbound.html', context)

@login_required
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

@login_required
@user_passes_test(is_manager)
def edit_inbound(request, pk):
    inbound_record = get_object_or_404(Inbound, pk=pk)
    original_quantity = inbound_record.quantity

    if request.method == 'POST':
        form = InboundForm(request.POST, instance=inbound_record)
        if form.is_valid():
            updated_record = form.save(commit=False)

            # Adjust the inventory quantity based on the updated inbound quantity
            quantity_difference = updated_record.quantity - original_quantity
            updated_record.product_sku.quantity += quantity_difference
            updated_record.product_sku.save()
            updated_record.save()
            messages.success(request, 'Record edited successfully.')
            return redirect('view_inbound_history')
    else:
        form = InboundForm(instance=inbound_record)

    context = {
        'form': form,
        'inbound_record': inbound_record,
    }
    return render(request, 'inventory/inbound/edit_inbound.html', context)

@login_required
@user_passes_test(is_manager)
def delete_inbound(request, pk):
    inbound_record = get_object_or_404(Inbound, pk=pk)
    
    if request.method == 'POST':
        # Revert the inventory quantity
        inbound_record.product_sku.quantity -= inbound_record.quantity
        inbound_record.product_sku.save()
        inbound_record.delete()
        messages.success(request, 'Record deleted successfully.')
        return redirect('view_inbound_history')

    context = {
        'inbound_record': inbound_record,
    }
    return render(request, 'inventory/inbound/delete_inbound.html', context)

# OUTBOUND
@login_required
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
                return redirect('view_outbound_history')
    else:
        form = OutboundForm()
        
    context = {
        'form': form
    }
    return render(request, 'inventory/record_outbound.html', context)

@login_required
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

@login_required
@user_passes_test(is_manager)
def edit_outbound(request, pk):
    outbound_record = get_object_or_404(Outbound, pk=pk)
    original_quantity = outbound_record.quantity

    if request.method == 'POST':
        form = OutboundForm(request.POST, instance=outbound_record)
        if form.is_valid():
            updated_record = form.save(commit=False)
            quantity_difference = original_quantity - updated_record.quantity
            updated_record.product_sku.quantity += quantity_difference  # Revert the outbound effect
            updated_record.product_sku.save()
            updated_record.save()
            messages.success(request, 'Record edited successfully.')
            return redirect('view_outbound_history')
    else:
        form = OutboundForm(instance=outbound_record)

    context = {
        'form': form,
        'outbound_record': outbound_record,
    }
    return render(request, 'inventory/outbound/edit_outbound.html', context)

@login_required
@user_passes_test(is_manager)
def delete_outbound(request, pk):
    outbound_record = get_object_or_404(Outbound, pk=pk)
    
    if request.method == 'POST':
        outbound_record.product_sku.quantity += outbound_record.quantity  # Revert the outbound effect
        outbound_record.product_sku.save()
        outbound_record.delete()
        messages.success(request, 'Record deleted successfully.')
        return redirect('view_outbound_history')

    context = {
        'outbound_record': outbound_record,
    }
    return render(request, 'inventory/outbound/delete_outbound.html', context)