from .models import Category, Product
from .forms import ProductSearchForm
from django.core import serializers
from django.shortcuts import render
from django.http import JsonResponse

def categories(request):
    return {"categories": Category.objects.all()}


def wishlist(request):
    if request.user.is_authenticated:
        wishlist = Product.objects.filter(users_wishlist=request.user)
        return {"wishlist": wishlist}
    else:
        return {"wishlist": []}



def search_data(request):
    form = ProductSearchForm()
    query = ''
    results = []
    return {
        'search_form':form,
        'query':query,
        'results':results}
