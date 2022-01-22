from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views
from django.views.generic import TemplateView

app_name = 'management'

urlpatterns = [
    #Store Management
    path('', TemplateView.as_view(template_name='management/main.html'), name='management'),
    
    #Products
    path('products/', views.ProductListView.as_view(), name='products'),
    path('products/edit/<slug:slug>/',views.ProductEditView.as_view(),name='edit_product'),
    path('products/delete/<slug:slug>/',views.ProductDeleteView.as_view(),name='delete_product'),
    path('products/add-new-product/',views.create_product,name='create_product'),
    
    # Product Types
    path('product-types/', views.ProductTypeListView.as_view(), name='product_types'),
    path('product-types/edit/<int:product_type_id>/',views.ProductTypeEditView.as_view(),name='edit_product_type'),
    path('product-types/delete/<int:product_type_id>/',views.ProductTypeDeleteView.as_view(),name='delete_product_type'),
    path('product-types/add-new-product-type/',views.ProductTypeCreateView.as_view(),name='add_product_type'),
    
    # Categories
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('categories/edit/<slug:slug>',views.CategoryEditView.as_view(),name='edit_category'),
    path('categories/delete/<slug:slug>',views.CategoryDeleteView.as_view(),name='delete_category'),
    path('categories/add-new-category/',views.CategoryCreateView.as_view(),name='create_category'),

    #Offers
    path('offers/', views.OfferListView.as_view(), name='offers'),
    path('offers/edit/<slug:slug>',views.OfferEditView.as_view(),name='edit_offer'),
    path('offers/delete/<slug:slug>',views.OfferDeleteView.as_view(),name='delete_offer'),
    path('offers/add-new-offer/',views.OfferCreateView.as_view(),name='create_offer'),
]