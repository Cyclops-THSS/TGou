"""TGouSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from . import views
from .forms import UserRegForm
from .short_cut import *
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import *

doNotLogin = lambda u: u.user.is_authenticated() == False

urlpatterns = [
    # accounts related
    # url(r'^accounts/profile/$', views.view_profile, name='view_profile'),
    url(r'^accounts/profile/edit/$', views.edit_profile, name='edit_profile'),
    url(r'^accounts/profile/$', views.view_profile, name='view_profile'),
    url(r'^accounts/register/$', check_request(doNotLogin, 'Please log out first!')(views.TRegistrationView.as_view()),
        name='registration_register'),
    url(r'^accounts/login/$', check_request(doNotLogin, 'Please log out first!')(auth_views.login), {'template_name': 'registration/login.html'},
        name='auth_login'),
    url(r'^accounts/logout/$', login_required(auth_views.logout),
        {'template_name': 'registration/logout.html'}, name='logout'),
    url(r'^accounts/', include('registration.backends.simple.urls')),

    # shop related
    url(r'^shop/$', views.search_shop, name='search_shop'),
    url(r'^shop/new$', views.new_shop, name='new_shop'),
    url(r'^shop/delete$', views.delete_shop, name='delete_shop'),
    url(r'^shop/edit$', views.edit_shop, name='edit_shop'),
    url(r'^shop/(?P<id>\d+)$', views.view_shop_id, name='view_shop_id'),
    url(r'^shop/(?P<name>\w+)$', views.view_shop_name, name='view_shop_name'),
	url(r'^shopincategory', views.view_shop_in_category, name='view_shop_in_category'),
	url(r'^shopcategories', views.view_shop_categories, name='view_shop_categories'),
    # cart related
    url(r'^cart/$', views.edit_cart, name='edit_cart'),
    url(r'^add-to-cart/$', views.add_to_cart, name='add-to-cart'),
    # order related
    url(r'^order/$', views.view_order, name='view_order'),
    url(r'^order/new$', views.new_order, name='new_order'),
    url(r'^order/(?P<id>\d+)$', views.view_order_id, name='view_order_id'),
    url(r'^order/(?P<id>\d+)/edit$', views.edit_order, name='edit_order'),
    url(r'^order/(?P<id>\d+)/confirm$', views.confirm_order, name='confirm_order'),
    url(r'^order/(?P<id>\d+)/delete$', views.delete_order, name='delete_order'),
    # product related
	url(r'^$', views.search_product, name='index'),
    url(r'^product/$', views.search_product, name='search_product'),
    url(r'^product/new$', views.new_product, name='new_product'),
    url(r'^product/(?P<id>\d+)$', views.view_product_id, name='view_product_id'),
    url(r'^product/(?P<id>\d+)/edit$', views.edit_product, name='edit_product'),
    url(r'^product/(?P<id>\d+)/delete$',
        views.delete_product, name='delete_product'),
	url(r'^productincategory', views.view_product_in_category, name='view_product_in_category'),
	url(r'^productcategories', views.view_product_categories, name='view_product_categories'),
    # comment related
    url(r'^comment/new$', views.new_comment, name='new_comment'),
    url(r'^comment/(?P<id>\d+)/edit$', views.edit_comment, name='edit_comment'),
    url(r'^comment/(?P<id>\d+)/delete$',
        views.delete_comment, name='delete_comment'),
    # grading related
    url(r'^grading/apply$', views.apply_grading, name='apply_grading'),
    # others (index: name='index')
    url(r'^error/$', views.error, name='error'),
]
