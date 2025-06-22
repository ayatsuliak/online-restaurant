from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('new/', views.create_order, name='create_order'),
    path('success/', views.order_success, name='order_success'),
    path('', views.order_list, name='order_list'),
]
