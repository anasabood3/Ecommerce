from os import stat
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render,get_object_or_404

from store.forms import CommentForm, ProductSearchForm
from .models import Category, Offer, Product, ProductSpecificationValue,Comment
from django.core import serializers

def home(request):
    categories = Category.objects.filter(is_active=True)
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
    # comments =Comment.objects.filter(product=product.id)
    comments = product.comments.filter(status=True)
    user_comment = None
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            user_comment = comment_form.save(commit=False)
            user_comment.product = product
            user_comment.user = request.user
            user_comment.user_name = f"{request.user.first_name} {request.user.last_name}"
            user_comment.save()
            return HttpResponseRedirect("/products/" + product.slug)
    else:
        comment_form = CommentForm()

    #check if product was in wishlist
    if request.user.is_authenticated:
        product_state = product.added_to_wishlist(request.user.id)
    else:
        product_state = False

     # ps = ProductSpecificationValue.objects.select_related('specification').filter(product_id = product.id)
    product_specs = ProductSpecificationValue.objects.raw('select * from store_productspecification join store_productspecificationvalue on store_productspecification.id = store_productspecificationvalue.specification_id where store_productspecificationvalue.product_id = ' + str(product.id) +';')
    return render(request, 'store/product_details.html', {'product': product,'product_state':product_state,'product_specs':product_specs,'comment_form':comment_form,'comments':comments})








def contact_us(request):
    return render(request,'store/contact_us.html')

def product_search(request):
    form = ProductSearchForm()
    q = ''
    results = []
    # handling suggestions
    if request.POST.get('action') == 'post':
        search_string = str(request.POST.get('ss'))
        if search_string is not None:
            search_string = Product.objects.filter(title__contains=search_string)[:3]
            data = serializers.serialize('json',list(search_string),fields=('id','title','slug'))
            return JsonResponse({'search_string':data})
    # handling search list
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
