from math import floor
from traceback import print_tb
from django.http import  HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic.base import View
from store.forms import CommentForm, ProductSearchForm
from .models import Category, Offer, Product, ProductSpecificationValue, Comment, Rate
from django.core import serializers
from django.db.models import Sum,Avg

def home(request):
    categories = Category.objects.filter(is_active=True)
    offers = Offer.objects.filter(is_active=True)
    return render(
        request, "store\index.html", {"catigories": categories, "offers": offers})



def contact_us(request):
    return render(request, "store/contact_us.html")


# View all products of all categories
def all_products(request):
    if request.is_ajax():
        action = request.GET.get('action')
        if action == 'quick_view':
            slug=request.GET.get('product')
            product = get_object_or_404(Product, slug=slug, is_active=True)
            response_data = {}
            response_data["title"] = product.title
            response_data["price"] = product.regular_price
            response_data["description"] = product.description
            response_data["image"] = product.product_image.get(is_feature=True).image.url

            return JsonResponse(response_data, status=200)
    else:
        products= Product.objects.filter(is_active=True)
        products = Product.objects.prefetch_related("product_image").filter(is_active=True)
        products_states = [p.added_to_wishlist(request.user.id) for p in products]
        return render(
        request, "store/category.html", {"products": zip(products, products_states)}
    )



class CategoryProductsListView(View):
    product = None

    def get(slef,request, slug_category=None):
        if request.is_ajax():
            action = request.GET.get('action')
            if action == 'quick_view':
                slug=request.GET.get('product')
                product = get_object_or_404(Product, slug=slug, is_active=True)
                response_data = {}
                response_data["title"] = product.title
                response_data["price"] = product.regular_price
                response_data["description"] = product.description
                response_data["image"] = product.product_image.get(is_feature=True).image.url

                return JsonResponse(response_data, status=200)
        else:
            category= get_object_or_404(Category,slug=slug_category)
            products = Product.objects.prefetch_related("product_image").filter(is_active=True, category=category)
            # should be enhanced
            products_states = [request.user.user_wishlist.filter(slug=p.slug).exists() for p in products]
            return render(request,"store/category.html",{"category": category, "products": zip(products, products_states)},)





class ProductDetails(View):
    user_comment = None
    def get(self, request, slug):
        # get the current product and user
        product = get_object_or_404(Product, slug=slug, is_active=True)
        curr_user=request.user

        # -------------Prepare product details to be renderend-------------


        # get product all specifacation (Waiting to convert into django ORM)
        # ps = ProductSpecificationValue.objects.select_related('specification').filter(product_id = product.id)
        product_specs = ProductSpecificationValue.objects.raw(
            "select * from store_productspecification join store_productspecificationvalue on store_productspecification.id = store_productspecificationvalue.specification_id where store_productspecificationvalue.product_id = "
            + str(product.id)
            + ";"
        )

        comments = product.comments.filter(status=True)
       


        rate = product.rates.all().aggregate(Avg('rate_value'))['rate_value__avg']
        if rate:
            product_rate=round(rate)
        else:
            product_rate = 0
        

        if curr_user.is_authenticated:
            product_state = curr_user.user_wishlist.filter(slug=product.slug).exists()
            product_user_rate=Rate.objects.filter(product=product,user=curr_user)
            if product_user_rate:
                user_rate=product_user_rate[0].rate_value
            else:
                user_rate="Still Not Rated"
            
            comment_form = CommentForm()
        else:
            product_state = False
            product_user_rate="Login to Rate"

        return render(
            request,
            "store/product_details.html",
            {
                "product": product,
                "product_state": product_state,
                "product_specs": product_specs,
                "comment_form": comment_form,
                "comments": comments,
                "product_rate":product_rate,
                "user_rating":user_rate,
            },
        )



    def post(self, request, slug):
        product = get_object_or_404(Product, slug=slug, is_active=True)

        if request.is_ajax:
            action = request.POST.get('action')

            if action == 'comment':

                comment_form =request.POST
                form = CommentForm(comment_form)

                if form.is_valid():
                    user_comment = form.save(commit=False)
                    user_comment.product = product
                    user_comment.user = request.user
                    user_comment.save()

                    #return reply/commen data
                    response_data = {}
                    # result means successeded or failed...
                    response_data["result"] = True
                    response_data["text"] = user_comment.content
                    response_data["created"] = user_comment.publish_date.strftime(
                        "%B %d, %Y %I:%M %p"
                    )
                    response_data["commenter"] = f"{request.user.first_name} {request.user.last_name}"

                    if user_comment.parent is None:
                        response_data["parent"] = None

                    else:
                        response_data["parent"] = user_comment.parent.pk

                    response_data["comment_id"] = user_comment.pk

                    return JsonResponse(response_data, status=200)
                
            elif action=="rate":
                rate_level = request.POST.get("rating_value")
                obj, _ = Rate.objects.get_or_create(product=product,user=request.user)
                obj.rate_value = rate_level
                obj.save()
                return JsonResponse({},status=200)

            elif action=="add_to_whishlist":

                product_slug = request.POST.get("product_id")
                product = get_object_or_404(Product, slug=product_slug)
                customer=request.user

                if customer.user_wishlist.filter(slug=product_slug).exists():
                    customer.user_wishlist.remove(product)
                    state=False
                else:
                    customer.user_wishlist.add(product)
                    state=True

                whish_list=customer.user_wishlist.count()

                return JsonResponse({"length_of_wishlist": whish_list,"decrease_amount":product.regular_price,"state":state}, status=200)





class ProductSearch(View):

    def get(self,request):
        form = ProductSearchForm()
        query = ""
        results = []
        if "query" in request.GET:
            form = ProductSearchForm(request.GET)
            if form.is_valid():
                query = form.cleaned_data["query"]
                results = Product.objects.filter(title__contains=query)
        return render(
        request, "store/search.html", {"form": form, "query": query, "results": results}
    )
    def post(self,request):
        action = request.POST.get('action')
        if request.is_ajax:
            if action=="search":
                search_string = str(request.POST.get("ss"))
                if search_string is not None:
                    print( search_string + ":search string were receivein successfully")
                    search_string = Product.objects.filter(title__contains=search_string)[:3]
                    data = serializers.serialize(
                        "json", list(search_string), fields=("id", "title", "slug")
                    )
                    return JsonResponse({"search_string": data})










# obselete

# def product_search(request):
    
#     # handling suggestions
#     if request.POST.get("action") == "post":
#         search_string = str(request.POST.get("ss"))
#         if search_string is not None:
#             search_string = Product.objects.filter(title__contains=search_string)[:3]
#             data = serializers.serialize(
#                 "json", list(search_string), fields=("id", "title", "slug")
#             )
#             return JsonResponse({"search_string": data})
    
#     # handling search list
#     if "query" in request.GET:
#         form = ProductSearchForm(request.GET)
#         if form.is_valid():
#             query = form.cleaned_data["query"]
#             results = Product.objects.filter(title__contains=query)

#     return render(
#         request, "store/search.html", {"form": form, "query": query, "results": results}
#     )
