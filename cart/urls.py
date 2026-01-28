from django.urls import path

from cart.dashboard import admin_dashboard
from . import views

urlpatterns = [
    path("cart/", views.cart_detail, name="cart_detail"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/update/<int:item_id>/", views.update_cart_item, name="update_cart_item"),
    path("checkout/", views.checkout, name="checkout"),
    path("admin-panel/", admin_dashboard, name="dashboard_analytics"),
    path("admin-panel/orders/", views.get_all_orders, name="admin_orders"),
    path(
        "orders/<int:order_id>/update-status/",
        views.update_order_status,
        name="update_order_status",
    ),
    path("admin-panel/customers/", views.admin_customers, name="admin_customers"),
    path("customers/", views.api_get_all_customers, name="api_customers"),
    path(
        "admin/customer/<int:customer_id>/orders/",
        views.customer_order_history,
        name="customer_order_history",
    ),
    path(
        "customer/<int:customer_id>/orders/",
        views.api_customer_orders,
        name="customer_orders",
    ),
    path("account/my-orders/", views.my_orders_view, name="my_orders"),
]
