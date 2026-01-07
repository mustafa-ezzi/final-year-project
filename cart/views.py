from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import Product
from .models import Cart, CartItem
from django.http import JsonResponse
import json


def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, "cart_detail.html", {"cart": cart})



def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        cart_item.quantity += 1
    cart_item.save()

    return redirect("cart_detail")



def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect("cart_detail")



def update_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)

    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        cart_item.quantity = max(1, quantity)
        cart_item.save()

    return redirect("cart_detail")


def update_cart_item(request, item_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')

        cart_item = CartItem.objects.get(id=item_id)
        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease' and cart_item.quantity > 1:
            cart_item.quantity -= 1

        cart_item.save()
        cart = cart_item.cart
        total_price = cart.total_price  # Your existing method
        return JsonResponse({
            'success': True,
            'quantity': cart_item.quantity,
            'subtotal': cart_item.subtotal,
            'total_price': total_price
        })
