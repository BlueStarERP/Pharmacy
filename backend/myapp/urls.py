from django.urls import path
from .views import *
# app_name = 'myapp'
urlpatterns = [
    path('', index, name='index'),
    path('customers/', customer_list, name='customer_list'),
    path('customers/<int:pk>/', customer_detail, name='customer_detail'),
    # path('about/', views.about, name='about'),
    # path('contact/', views.contact, name='contact'),
]