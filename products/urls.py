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
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
