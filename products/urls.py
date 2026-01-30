from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path("admin-panel/products", views.index, name="index"),
    path("", views.home, name="home"),
    path("insert/", views.insertData, name="insert"),
    path("update/<int:id>/", views.updateData, name="update"),
    path("delete/<int:id>/", views.deleteData, name="delete"),
    path("product/<int:id>/", views.viewProduct, name="view-product"),
    path('about/', views.about, name='about'),
    path('admin-verify/', views.admin_login_verify, name='admin_login_verify'),
path('admin-logout/', views.admin_logout, name='admin_logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
