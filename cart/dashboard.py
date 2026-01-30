from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, Count, Q
from django.utils.timezone import now
from .models import Order, OrderItem
from products.models import Product
from user_register.models import Customer

def admin_dashboard(request):
    today_date = now().date()

    stats = Order.objects.aggregate(
        total_count=Count('id'),
        paid_count=Count('id', filter=Q(is_paid=True)),
        total_revenue=Sum('total_amount'),
        today_revenue=Sum('total_amount', filter=Q(created_at__date=today_date))
    )

    context = {
        # Changed this to total_sales to match your HTML
        "total_sales": stats['total_revenue'] or 0, 
        "active_orders": stats['total_count'] or 0,
        "today_sales": stats['today_revenue'] or 0,
        "total_products": Product.objects.count(),
        "total_customers": Customer.objects.count(),
        "recent_orders": Order.objects.select_related("customer").order_by("-created_at")[:8],
        # Added 'products' so your "Latest Arrivals" sidebar works
        "products": Product.objects.all().order_by("-id")[:5], 
    }
    return render(request, "admin_dashboard.html", context)