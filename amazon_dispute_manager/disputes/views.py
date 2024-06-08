# disputes/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Item, Order, Return, Dispute, Seller, CustomUser
from .forms import OrderForm, ReturnForm, DisputeForm, ItemForm
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import login, authenticate


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.role == 'seller':
                Seller.objects.create(user=user, name=user.username)
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def custom_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if request.user.role == 'seller':
                    return redirect('item_list')
                elif request.user.role == 'customer':
                    return redirect('order_list')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def item_list(request):
    seller = get_object_or_404(Seller, user=request.user)
    items = Item.objects.filter(seller=seller)
    return render(request, 'disputes/item_list.html', {'items': items})


@login_required
def order_list(request):
    if request.user.role == 'seller':
        seller = get_object_or_404(Seller, user=request.user)
        orders = Order.objects.filter(item__seller=seller)
    if request.user.role == 'customer':
        orders = Order.objects.filter(customer=request.user)
    return render(request, 'disputes/order_list.html', {'orders': orders})


@login_required
def return_list(request):
    seller = get_object_or_404(Seller, user=request.user)
    returns = Return.objects.filter(order__item__seller=seller)
    return render(request, 'disputes/return_list.html', {'returns': returns})


@login_required
def dispute_list(request):
    seller = get_object_or_404(Seller, user=request.user)
    disputes = Dispute.objects.filter(return_order__order__item__seller=seller)
    return render(request, 'disputes/dispute_list.html', {'disputes': disputes})


@login_required
def create_dispute(request, return_id):
    seller = get_object_or_404(Seller, user=request.user)
    return_order = get_object_or_404(Return, id=return_id, order__item__seller=seller)
    if request.method == 'POST':
        form = DisputeForm(request.POST)
        if form.is_valid():
            dispute = form.save(commit=False)
            dispute.return_order = return_order
            dispute.save()
            return redirect('dispute_list')
    else:
        form = DisputeForm()
    return render(request, 'disputes/create_dispute.html', {'form': form, 'return_order': return_order})


@login_required
def create_item(request):
    seller = get_object_or_404(Seller, user=request.user)
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.seller = seller
            item.save()
            return redirect('item_list')
    else:
        form = ItemForm()
    return render(request, 'disputes/create_item.html', {'form': form})


@login_required
def create_order(request):
    if request.user.role != 'customer':
        return redirect('home')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = request.user
            order.save()
            return redirect('order_list')
    else:
        form = OrderForm()
    return render(request, 'disputes/create_order.html', {'form': form})
