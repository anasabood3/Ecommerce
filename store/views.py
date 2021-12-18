from django.shortcuts import render,get_object_or_404
from .models import Category, Product, ProductSpecification


def home(request):
    category = Category.objects.all()
    return render(request,'store\index.html',{'catigories':category})


def category_products(request,slug_category=None):
    category = get_object_or_404(Category,slug=slug_category)
    # products = Product.objects.filter(category = category)
    products = Product.objects.prefetch_related("product_image").filter(is_active=True,category = category)
    return render(request, 'store/category.html',{'category':category,'products':products})

def all_products(request):
    products = Product.objects.filter(is_active=True)
    return render(request, 'store/category.html',{'products':products})

def product_details(request,slug):

    product = get_object_or_404(Product, slug=slug, is_active=True)
    # productspecification = get_object_or_404(ProductSpecification, slug=slug, is_active=True)
    return render(request, 'store/product_details.html', {'product': product})

# def product_all(request):
#     products = Product.objects.prefetch_related("product_image").filter(is_active=True)
#     return render(request, "store/index.html", {"products": products})
def contact_us(request):
    return render(request,'store/contact_us.html')