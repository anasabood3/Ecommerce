from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views



app_name = 'store'

urlpatterns = [
    path('',views.home,name='home'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('products/<slug:slug>',views.product_details,name='product_detail'),
    path('shop/all/', views.all_products, name='all_products'),
    path('shop/<slug:slug_category>/', views.category_products, name='category_list'),

]
