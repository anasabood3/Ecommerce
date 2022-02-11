from .models import Category, Product
from .forms import ProductSearchForm
from django.core import serializers
from django.shortcuts import render
from django.http import JsonResponse

def categories(request):
    return {"categories": Category.objects.filter(level=0)}


def wishlist(request):
    if request.user.is_authenticated:
        wishlist = Product.objects.filter(users_wishlist=request.user)
        return {"wishlist": wishlist}
    else:
        return {"wishlist": []}



def search_data(request):
    form = ProductSearchForm()
    q = ''
    results = []
    return {
        'search_form':form,
        'q':q,
        'results':results}
