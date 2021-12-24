from .models import Category, Product


def categories(request):
    return {"categories": Category.objects.filter(level=0)}


def wishlist(request):
    wishlist = Product.objects.filter(users_wishlist=request.user)
    return {"wishlist": wishlist}
