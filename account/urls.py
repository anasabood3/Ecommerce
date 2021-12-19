from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views
from .forms import PwdResetConfirmForm, PwdResetForm, UserLoginForm, PwdChangeForm
from django.views.generic import TemplateView

app_name = 'account'

urlpatterns = [
    # Registration
    path('register/', views.account_register, name='register'),
    path('activate/<slug:uidb64>/<slug:token>)/', views.account_activate, name='activate'),
    # Aythentication
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html', form_class=UserLoginForm,
                                                redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/account/login'), name='logout'),
    # Paswword Reset
    path('password_reset/',
         auth_views.PasswordResetView.as_view(template_name="account/password_reset/password_reset_form.html",
                                              success_url='password_reset_email_confirm',
                                              email_template_name='account/password_reset/password_reset_email.html',
                                              form_class=PwdResetForm), name='pwdreset'),
    path('password_reset_confirm/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset/password_reset_confirm.html',
                                                     success_url='password_reset_complete/',
                                                     form_class=PwdResetConfirmForm),
         name="password_reset_confirm"),
    path('password_reset/password_reset_email_confirm/',
         TemplateView.as_view(template_name="account/password_reset/reset_status.html"), name='password_reset_done'),
    path('password_reset_confirm/<token>/password_reset_complete/',
         TemplateView.as_view(template_name="account/password_reset/reset_status.html"),
         name='password_reset_complete'),
    # Password Change
    path('profile/edit/password_change/',auth_views.PasswordChangeView.as_view(template_name='account/dashboard/password_change.html',success_url='password_change_completed',form_class=PwdChangeForm),name='pwdchange'),
    path('profile/edit/password_change/password_change_completed/',auth_views.PasswordChangeDoneView.as_view(template_name='account/dashboard/dashboard.html'),name='pwdchange_done'),
    #Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/edit/', views.edit_details, name='edit_details'),
    path('profile/delete_user/', views.delete_user, name='delete_user'),
    path('profile/delete_confirm/', TemplateView.as_view(template_name="account/dashboard/delete_confirm.html"),name='delete_confirmation'),

    # Wish List
    # path("wishlist/add_to_wishlist/<int:id>", views.add_to_wishlist, name="users_wishlist"),
    path("wishlist/add_to_wishlist/", views.add_to_wishlist, name="users_wishlist"),
    path("wishlist/", views.wishlist, name="wishlist"),
]
