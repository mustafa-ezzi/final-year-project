from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Cart, CartItem, Order, OrderItem
from products.models import Product
from user_register.models import Customer
import json
from django.contrib.auth.decorators import login_required
from django.db.models import Sum,Count
from django.db import transaction
from django.views.decorators.http import require_POST

# ---------------- CART DETAIL ----------------
def cart_detail(request):
    cart = None
    cart_id = request.session.get("cart_id")

    if cart_id:
        cart = Cart.objects.filter(id=cart_id).first()

    return render(request, "cart_detail.html", {"cart": cart})


# ---------------- ADD TO CART ----------------
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_id = request.session.get("cart_id")

    if cart_id:
        # Using filter().first() is safer than get() to avoid 404/MultipleObjects errors
        cart = Cart.objects.filter(id=cart_id).first()
        if not cart:  # In case session has a dead ID
            cart = Cart.objects.create()
            request.session["cart_id"] = cart.id
    else:
        cart = Cart.objects.create()
        request.session["cart_id"] = cart.id

    item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        item.quantity += 1
        item.save()

    # --- NEW: Calculate totals for the JavaScript ---
    # Total count of items
    total_items = cart.items.aggregate(Sum("quantity"))["quantity__sum"] or 0

    # Total price (This assumes your CartItem has a price or calculates from product)
    # If your model structure is different, adjust this calculation
    total_price = 0
    for cart_item in cart.items.all():
        total_price += cart_item.product.price * cart_item.quantity

    # Return JSON instead of a redirect
    return JsonResponse(
        {
            "success": True,
            "cart_count": total_items,
            "cart_total": f"{total_price:,}",  # Formats with commas like 15,000
        }
    )


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
                "subtotal": cart_item.subtotal,  # no ()
                "total_price": cart.total_price,  # no ()
            }
        )


# ---------------- CHECKOUT ----------------
@transaction.atomic
def checkout(request):
    cart_id = request.session.get("cart_id")
    if not cart_id:
        return redirect("cart_detail")

    cart = Cart.objects.filter(id=cart_id).first()
    if not cart or cart.items.count() == 0:
        return redirect("cart_detail")

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")

            # 1. Check if user exists by email for the "Welcome Back" logic
            # We check this BEFORE get_or_create to determine user status
            user_exists = Customer.objects.filter(email=email).exists()

            # 2. Customer Registration/Lookup
            # We use email or phone_number depending on your unique constraint
            customer, created = Customer.objects.get_or_create(
                email=email,
                defaults={
                    "first_name": data.get("first_name"),
                    "last_name": data.get("last_name"),
                    "phone_number": data.get("phone_number"),
                    "address": data.get("address"),
                    "delivery_type": "home",
                },
            )

            # Store the name in the session for the Navbar to update
            request.session["customer_name"] = customer.first_name

            # 3. Total Calculation
            shipping_cost = float(data.get("shipping_cost", 0))
            grand_total = float(cart.total_price) + shipping_cost

            # 4. Create Order
            order = Order.objects.create(
                customer=customer,
                shipping_address=data.get("address", ""),
                city=data.get("city", ""),
                state=data.get("state", ""),
                zip_code=data.get("zip", ""),
                total_amount=grand_total,
            )

            # 5. Create Order Items
            items = [
                OrderItem(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity,
                )
                for item in cart.items.all()
            ]
            OrderItem.objects.bulk_create(items)

            # 6. Cleanup Cart
            cart.items.all().delete()
            request.session.pop("cart_id", None)

            # 7. Return status instead of redirecting
            return JsonResponse(
                {
                    "success": True,
                    "user_status": "returning" if user_exists else "new",
                    "customer_name": customer.first_name,
                    "order_id": order.id,
                }
            )

        except Exception as e:
            return JsonResponse(
                {"success": False, "message": f"Error: {str(e)}"}, status=500
            )

    return render(request, "checkout.html", {"cart": cart})


def get_all_orders(request):
    # Optimized QuerySet
    orders = (
        Order.objects.select_related("customer")
        .prefetch_related("items", "items__product")
        .order_by("-created_at")
    )

    # Note: We no longer need the 'data' list loop at all!
    # Django handles the 'Guest' logic directly in the template.
    
    return render(request, "admin_orders.html", {"orders": orders})


@require_POST
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    new_status = request.POST.get('status')
    
    if new_status in [Order.STATUS_PENDING, Order.STATUS_DISPATCHED, Order.STATUS_COMPLETED]:
        order.status = new_status
        # Optional: Auto-mark as paid if completed
        if new_status == Order.STATUS_COMPLETED:
            order.is_paid = True
        order.save()
        
    return redirect('admin_orders')

def admin_customers(request):
    # Fetch customers and calculate their stats on the fly
    customers = Customer.objects.annotate(
        order_count=Count('order'),
        total_spent=Sum('order__total_amount')
    ).order_by('-total_spent')  # Highest spenders first

    return render(request, "admin_customers.html", {"customers": customers})


def api_get_all_customers(request):
    customers = Customer.objects.all().values('id', 'first_name', 'last_name', 'email', 'phone_number')
    return JsonResponse({"customers": list(customers)}, safe=False)

def customer_order_history(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    # Get all orders for this customer, newest first
    orders = Order.objects.filter(customer=customer).order_by('-created_at')
    
    context = {
        'customer': customer,
        'orders': orders,
    }
    return render(request, 'customer_orders.html', context)

# 2. API View (JSON)
def api_customer_orders(request, customer_id):
    orders = Order.objects.filter(customer_id=customer_id).values(
        'id', 'total_amount', 'is_paid', 'status', 'created_at'
    )
    return JsonResponse({"customer_id": customer_id, "orders": list(orders)})

def my_orders_view(request):
    # Get customer ID from session (set during login)
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return redirect('login') # Or wherever your login is
        
    customer = get_object_or_404(Customer, id=customer_id)
    orders = Order.objects.filter(customer=customer).order_by('-created_at')
    
    return render(request, 'customer_orders.html', {
        'customer': customer,
        'orders': orders,
    })

