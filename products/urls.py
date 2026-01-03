from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('admin-panel/', views.index, name='index'),
    path('insert/', views.insertData, name='insert'),
    path('update/<int:id>/', views.updateData, name='update'),
    path('delete/<int:id>/', views.deleteData, name='delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)