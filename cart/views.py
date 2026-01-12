from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Cart, CartItem, Order, OrderItem
from products.models import Product
from user_register.models import Customer
import json


# ---------------- CART DETAIL ----------------
def cart_detail(request):
    customer_id = request.session.get("customer_id")
    if not customer_id:
        return redirect("login")

    customer = Customer.objects.get(id=customer_id)
    cart, created = Cart.objects.get_or_create(user=customer)
    return render(request, "cart_detail.html", {"cart": cart})


# ---------------- ADD TO CART ----------------
def add_to_cart(request, product_id):
    customer_id = request.session.get("customer_id")
    if not customer_id:
        return redirect("login")

    customer = Customer.objects.get(id=customer_id)
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=customer)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    return redirect("cart_detail")


# ---------------- REMOVE ITEM ----------------
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
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
    customer_id = request.session.get("customer_id")
    if not customer_id:
        return redirect("login")

    customer = get_object_or_404(Customer, id=customer_id)
    cart, _ = Cart.objects.get_or_create(user=customer)

    if not cart.items.exists():
        return redirect("cart_detail")  # no items → back to cart

    if request.method == "POST":
        try:
            data = json.loads(request.body)

            # Create Order
            order = Order.objects.create(
                user=customer,  # assuming Customer is your user model or adjust
                shipping_address=data.get("address", ""),
                city=data.get("city", ""),
                state=data.get("state", ""),
                zip_code=data.get("zip", ""),
                total_amount=cart.total_price(),
            )

            # Create OrderItems from CartItems
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,  # snapshot
                    quantity=item.quantity,
                )

            # Clear cart after successful order creation
            cart.items.all().delete()

            # In real app: here you would redirect to payment gateway
            # For now: success message / thank you page
            return JsonResponse(
                {
                    "success": True,
                    "message": "Order placed successfully!",
                    "order_id": order.id,
                }
            )

        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=400)

    # GET: show checkout form
    return render(
        request,
        "checkout.html",
        {
            "cart": cart,
            "customer": customer,  # prefill form if you want
        },
    )
