from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.forms.models import model_to_dict
from store.models import Product
from .forms import RegistrationForm, UserEditForm
from .models import UserBase
from .tokens import account_activation_token
from django.contrib import messages


#User Settings' Panel
@login_required
def dashboard(request):
    return render(request, "account/dashboard/dashboard.html")

#Wishlist Page
@login_required
def wishlist(request):
    products = Product.objects.filter(users_wishlist=request.user)
    total_price = 0
    #to_be_updated
    for i in products:total_price += i.regular_price
    return render(request, "account/dashboard/wishlist(2).html", {"wishlist": products,'total_price':total_price})

#Wishlist Managment
@login_required
def add_to_wishlist(request):
    if request.user.authenticated:
        print('Fuck You')
        if request.method == "POST":
            if request.is_ajax():
                product_id = request.POST.get("product_id")
                product = get_object_or_404(Product, id=product_id)
                # if prpduct is already  exist then remove it
                if product.users_wishlist.filter(id=request.user.id).exists():
                    product.users_wishlist.remove(request.user)
                    state = False
                # Or add it if it was not there
                else:
                    product.users_wishlist.add(request.user)
                    state = True
                length_of_wishlist = (product.users_wishlist  # M2M Manager
                    .through  # subjects_students through table
                .objects  # through table manager
                .filter(userbase_id=request.user.id)  # your query against through table
                .count())
                return JsonResponse({"length_of_wishlist": length_of_wishlist, "state":state}, status=200)
    else:
        return redirect("account:login")

# Usre Registration
def account_register(request):
    # if user already logged in
    if request.user.is_authenticated:
        return redirect("account:dashboard")
    # Else create a new account
    if request.method == "POST":
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data["email"]
            user.user_name = registerForm.cleaned_data["user_name"]
            user.set_password(registerForm.cleaned_data["password"])
            user.is_active = False
            user.save()
            # Setup Email
            current_site = get_current_site(request)
            subject = "Activate your Account"
            message = render_to_string(
                "account/registration/account_activation_email.html",
                {
                    "password_reset": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            user.email_user(subject=subject, message=message)
            return render(request, "account/registration/register_confirm.html")
    else:
        registerForm = RegistrationForm()
    return render(request, "account/registration/register.html", {"form": registerForm})


def account_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
    except:
        return HttpResponse("Somthing went wrong... ¯\_(*_*)_/¯")
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request,"Your Account were Successfully Activated")
        return redirect("account:dashboard")
    else:
        return render(request, "account/registration/activation_invalid.html")


#Edit User Details
@login_required
def edit_details(request):
    if request.method == "POST":
        user_form = UserEditForm(request.POST,request.FILES,instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request,"Changes were saved successfully")
    else:
        user_form = UserEditForm(instance=request.user)
    return render(request, "account/dashboard/user_info.html", {"user_form": user_form})

#Delete User Account
@login_required
def delete_user(request):
    if request.method == "POST":
        if request.is_ajax():
            user = UserBase.objects.get(user_name=request.user)
            if request.POST.get("confirm_delete") == "true":
                user.is_active = False
                user.save()
                logout(request)
                state = True
                error = ""
            else:
                state = False
                error = "You must Confirm The Deletion First"
            return JsonResponse({"state": state, "error": error}, status=200)



