
from django.urls import path

from user_register import views

urlpatterns = [
    path('',views.index, name='index'),
    # path('view',views.view, name='view'),
    path('insert-data', views.insertData, name='insertData' ),
    path('view-data', views.viewData, name='viewData' ),
    path('update/<id>', views.updateData, name='updateData' ),
    path('delete/<id>', views.deletData, name='deleteData' ),
]    
