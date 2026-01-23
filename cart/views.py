from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Cart, CartItem, Order, OrderItem
from products.models import Product
from user_register.models import Customer
import json
from django.contrib.auth.decorators import login_required


# ---------------- CART DETAIL ----------------
def cart_detail(request):
    cart = None
    cart_id = request.session.get('cart_id')

    if cart_id:
        cart = Cart.objects.filter(id=cart_id).first()

    return render(request, 'cart_detail.html', {
        'cart': cart
    })


# ---------------- ADD TO CART ----------------
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart_id = request.session.get('cart_id')

    if cart_id:
        cart = Cart.objects.get(id=cart_id)
    else:
        cart = Cart.objects.create()
        request.session['cart_id'] = cart.id

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        item.quantity += 1
        item.save()

    return redirect('cart_detail')


# ---------------- REMOVE ITEM ----------------

def remove_from_cart(request, item_id):
    cart_id = request.session.get("cart_id")

    if cart_id:
        item = get_object_or_404(CartItem, id=item_id, cart_id=cart_id)
        item.delete()

    return redirect("cart_detail")



# ---------------- UPDATE QUANTITY ----------------
def update_cart_item(request, item_id):
    if request.method == "POST":
        data = json.loads(request.body)
        action = data.get("action")

        cart_item = CartItem.objects.get(id=item_id)
        if action == "increase":
            cart_item.quantity += 1
        elif action == "decrease" and cart_item.quantity > 1:
            cart_item.quantity -= 1

        cart_item.save()
        cart = cart_item.cart
        return JsonResponse(
            {
                "success": True,
                "quantity": cart_item.quantity,
                "subtotal": cart_item.subtotal(),
                "total_price": cart.total_price(),
            }
        )


# ---------------- CHECKOUT ----------------
def checkout(request):
    # 1. Require login
    customer_id = request.session.get("customer_id")
    if not customer_id:
        return redirect("login")

    customer = get_object_or_404(Customer, id=customer_id)

    # 2. Get session cart
    session_cart = request.session.get("cart", {})
    if not session_cart:
        return redirect("cart_detail")

    # 3. Create / get DB cart
    cart, created = Cart.objects.get_or_create(user=customer)

    # 4. Sync session cart → DB cart
    cart.items.all().delete()  # prevent duplicates

    total = 0
    for product_id, qty in session_cart.items():
        product = Product.objects.get(id=product_id)
        CartItem.objects.create(
            cart=cart,
            product=product,
            quantity=qty
        )
        total += product.price * qty

    # 5. POST → place order
    if request.method == "POST":
        data = json.loads(request.body)

        order = Order.objects.create(
            user=customer,
            shipping_address=data.get("address", ""),
            city=data.get("city", ""),
            state=data.get("state", ""),
            zip_code=data.get("zip", ""),
            total_amount=total,
        )

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity,
            )

        # Clear both carts
        cart.items.all().delete()
        del request.session["cart"]

        return JsonResponse({
            "success": True,
            "order_id": order.id
        })

    # 6. GET → show checkout page
    return render(request, "checkout.html", {
        "cart": cart,
        "customer": customer
    })
