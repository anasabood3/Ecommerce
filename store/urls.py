from django.contrib.auth import views as auth_views
from django.urls import path
from . import views



app_name = 'store'

urlpatterns = [
    # Home page
    path('',views.home,name='home'),

    path('contact_us/', views.contact_us, name='contact_us'),
    # Product details
    path('products/<slug:slug>',views.ProductDetails.as_view(),name='product_detail'),
    # All Products 
    path('shop/all/', views.all_products, name='all_products'),
    # Products of specific category
    path('shop/<slug:slug_category>/', views.CategoryProductsListView.as_view(), name='category_list'),
    # Find Product
    path('search/',views.product_search,name='product_search')
]
