# disputes/views.py
import datetime

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
    if request.user.role == 'seller':
        seller = get_object_or_404(Seller, user=request.user)
        items = Item.objects.filter(seller=seller)
    if request.user.role == 'customer':
        items = Item.objects.all()
    return render(request, 'items/item_list.html', {'items': items, 'request': request})


@login_required
def order_list(request):
    if request.user.role == 'seller':
        seller = get_object_or_404(Seller, user=request.user)
        orders = Order.objects.filter(item__seller=seller)
    if request.user.role == 'customer':
        orders = Order.objects.filter(customer=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def return_list(request):
    seller = get_object_or_404(Seller, user=request.user)
    returns = Return.objects.filter(order__item__seller=seller)
    return render(request, 'returns/return_list.html', {'returns': returns})


@login_required
def dispute_list(request):
    seller = get_object_or_404(Seller, user=request.user)
    disputes = Dispute.objects.filter(return_order__order__item__seller=seller)
    return render(request, 'disputes/dispute_list.html', {'disputes': disputes})


@login_required
def dispute_view(request, dispute_id):
    dispute = get_object_or_404(Dispute, id=dispute_id)
    seller = get_object_or_404(Seller, user=request.user)
    if dispute.return_order.order.item.seller != seller:
        return redirect('dispute_list')

    if request.method == 'DELETE':
        dispute.delete()
        return HttpResponse(status=204)
    return render(request, 'disputes/view_dispute.html', {'dispute': dispute, 'request': request})


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
def edit_dispute(request, dispute_id):
    dispute = get_object_or_404(Dispute, id=dispute_id)
    seller = get_object_or_404(Seller, user=request.user)

    # Ensure the dispute belongs to a return order of the seller
    if dispute.return_order.order.item.seller != seller:
        return redirect('dispute_list')

    if request.method == 'POST':
        form = DisputeForm(request.POST, instance=dispute)
        if form.is_valid():
            form.save()
            return redirect('dispute_list')
    else:
        form = DisputeForm(instance=dispute)

    return render(request, 'disputes/edit_dispute.html', {'form': form, 'dispute': dispute})


@login_required
def delete_dispute(request, dispute_id):
    dispute = get_object_or_404(Dispute, id=dispute_id)
    seller = get_object_or_404(Seller, user=request.user)

    # Ensure the dispute belongs to a return order of the seller
    if dispute.return_order.order.item.seller != seller:
        return redirect('dispute_list')

    if request.method == 'DELETE':
        dispute.delete()
        return redirect('dispute_list')

    return render(request, 'disputes/delete_dispute.html', {'dispute': dispute})


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
    return render(request, 'items/create_item.html', {'form': form})


@login_required
def edit_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm(instance=item)
    return render(request, 'items/edit_item.html', {'form': form, 'item': item})


@login_required
def create_order(request, item_id):
    if request.user.role != 'customer':
        return redirect('item_list')

    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        order = Order()
        order.customer = request.user
        order.item = item
        order.date_ordered = datetime.datetime.now()
        order.save()
        return redirect('item_list')
    else:
        form = OrderForm()
        form.customer = request.user.customer
    return render(request, 'orders/create_order.html', {'form': form, 'item': item})


@login_required
def create_return(request, order_id):
    if request.user.role != 'customer':
        return redirect('item_list')

    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        return_order = Return()
        return_order.order = order
        return_order.return_reason = "test return"
        return_order.return_tracking = "pending"
        return_order.date_returned = datetime.datetime.now()
        return_order.save()
        order.status = 'Returned'
        order.save()
        return redirect('order_list')
    else:
        form = ReturnForm()
        form.order = order
    return render(request, 'returns/create_return.html', {'form': form, 'return': order})


@login_required
def edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm(instance=order)
    return render(request, ' orders/edit_order.html', {'form': form, 'order': order})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.http import Http404, HttpResponse
from .forms import *


def profile_view(request, username=None):
    if username:
        profile = get_object_or_404(CustomUser, username=username).profile
    else:
        try:
            profile = request.user.profile
        except:
            raise Http404()

    posts = profile.user.posts.all()

    context = {
        'profile': profile,
        'posts': posts,
    }

    return render(request, 'a_users/profile.html', context)


@login_required
def profile_edit_view(request):
    form = ProfileForm(instance=request.user.profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()

            if request.user.emailaddress_set.get(primary=True).verified:
                return redirect('profile')
            else:
                return redirect('profile-verify-email')

    if request.path == reverse('profile-onboarding'):
        template = 'a_users/profile_onboarding.html'
    else:
        template = 'a_users/profile_edit.html'

    return render(request, template, {'form': form})


@login_required
def profile_delete_view(request):
    user = request.user

    if request.method == 'POST':
        logout(request)
        user.delete()
        messages.success(request, 'Account deleted, what a pity')
        return redirect('home')

    return render(request, 'a_users/profile_delete.html')
