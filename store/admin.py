from django import forms
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from mptt.admin import MPTTModelAdmin

from .models import (
    Category,
    Product,
    ProductImage,
    ProductSpecification,
    ProductSpecificationValue,
    ProductType,
    Offer,
    Comment,
)

admin.site.register(Category, MPTTModelAdmin)


class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    inlines = [
        ProductSpecificationInline,
    ]


class ProductImageInline(admin.TabularInline):
    model = ProductImage


class ProductSpecificationValueInline(admin.TabularInline):
    model = ProductSpecificationValue


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductSpecificationValueInline,
        ProductImageInline,
    ]

admin.site.register(Offer)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("product","user_name","publish_date")
    list_filter = ("status","publish_date")
    search_fields = ("user_name","content")
