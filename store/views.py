from django.shortcuts import render,get_object_or_404

from store.forms import ProductSearchForm
from .models import Category, Offer, Product


def home(request):
    categories = Category.objects.all()
    offers = Offer.objects.all()
    return render(request,'store\index.html',{'catigories':categories,'offers':offers})


def category_products(request,slug_category=None):
    category = get_object_or_404(Category,slug=slug_category)
    # products = Product.objects.filter(category = category)
    products = Product.objects.prefetch_related("product_image").filter(is_active=True,category = category)
    products_states = [p.added_to_wishlist(request.user.id) for p in products]
    return render(request, 'store/category.html',{'category':category,'products':zip(products,products_states)})

def all_products(request):
    products = Product.objects.filter(is_active=True)
    products_states = [p.added_to_wishlist(request.user.id) for p in products]
    return render(request, 'store/category.html',{'products':zip(products,products_states)})

def product_details(request,slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    #check if product was in wishlist
    if request.user.is_authenticated:
        product_state = product.added_to_wishlist(request.user.id)
    else:
        product_state = False
    # productspecification = get_object_or_404(ProductSpecification, slug=slug, is_active=True)
    return render(request, 'store/product_details.html', {'product': product,'product_state':product_state})

def contact_us(request):
    return render(request,'store/contact_us.html')

def product_search(request):
    form = ProductSearchForm()
    q = ''
    results = []

    if 'q' in request.GET:
        form = ProductSearchForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data['q']
            results = Product.objects.filter(title__contains = q)
    return render(request, 'store/search.html',
    {
        'form':form,
        'q':q,
        'results':results
    })
