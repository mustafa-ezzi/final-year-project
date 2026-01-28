from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, Count, Q
from django.utils.timezone import now
from .models import Order, OrderItem
from products.models import Product
from user_register.models import Customer

def admin_dashboard(request):
    today_date = now().date()
    month_start = today_date.replace(day=1)

    # Use aggregate with default values to prevent "None" errors in HTML
    stats = Order.objects.aggregate(
        total_count=Count('id'),
        paid_count=Count('id', filter=Q(is_paid=True)),
        total_revenue=Sum('total_amount'),
        today_revenue=Sum('total_amount', filter=Q(created_at__date=today_date))
    )

    # Top Sellers logic
    top_products = OrderItem.objects.values(
        "product__name", "product__image"
    ).annotate(total_sold=Sum("quantity")).order_by("-total_sold")[:5]

    context = {
        # Ensuring we return 0 if the DB is empty
        "total_revenue": stats['total_revenue'] or 0,
        "active_orders": stats['total_count'] or 0,
        "today_sales": stats['today_revenue'] or 0,
        "total_products": Product.objects.count(),
        "total_customers": Customer.objects.count(),
        "recent_orders": Order.objects.select_related("customer").order_by("-created_at")[:8],
        "top_products": top_products,
    }
    return render(request, "admin_dashboard.html", context)

def all_orders(request):
    # This view powers the dedicated Orders Management page
    orders = Order.objects.select_related("customer").prefetch_related("items").order_by("-created_at")
    return render(request, "admin_orders.html", {"orders": orders})