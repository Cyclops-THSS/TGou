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


urlpatterns = [
    # accounts related
    url(r'^accounts/profile/$', views.view_profile, name='view_profile'),
    url(r'^accounts/profile/edit/$', views.edit_profile, name='edit_profile'),
    url(r'^accounts/register/$', views.TRegistrationView.as_view(),
        name='registration_register'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    # shop related
    url(r'^shop/$', views.view_shop, name='view_shop'),
    url(r'^shop/new$', views.new_shop, name='new_shop'),
    url(r'^shop/delete$', views.delete_shop, name='delete_shop'),
    url(r'^shop/edit$', views.edit_shop, name='edit_shop'),
    url(r'^shop/order/$', views.view_shop_orders, name='view_shop_orders'),
    url(r'^shop/search$', views.search_shop, name='search_shop'),
    url(r'^shop/(?P<id>\d+)$', views.view_shop_id, name='view_shop_id'),
    url(r'^shop/(?P<name>\w+)$', views.view_shop_name, name='view_shop_name'),
    # cart related
    url(r'^cart/$', views.edit_cart, name='edit_cart'),
    url(r'^cart/clear$', views.clear_cart, name='clear_cart'),
    # order related
    url(r'^order/$', views.view_order, name='view_order'),
    url(r'^order/new$', views.new_order, name='new_order'),
    url(r'^order/(?P<id>\d+)$', views.view_order_id, name='view_order_id'),
    url(r'^order/(?P<id>\d+)/edit$', views.edit_order, name='edit_order'),
    url(r'^order/(?P<id>\d+)/confirm$', views.confirm_order, name='confirm_order'),
    url(r'^order/(?P<id>\d+)/delete$', views.delete_order, name='delete_order'),
    # product related
    url(r'^product/$', views.view_product, name='view_product'),
    url(r'^product/search$', views.search_product, name='search_product'),
    url(r'^product/(?P<id>\d+)$', views.view_product_id, name='view_product_id'),
    url(r'^product/(?P<id>\d+)/edit$', views.edit_product, name='edit_product'),
    url(r'^product/(?P<id>\d+)/delete$',
        views.delete_product, name='delete_product'),
    # comment related
    url(r'^comment/new$', views.new_comment, name='new_comment'),
    url(r'^comment/edit/(?P<id>\d+)$', views.edit_comment, name='edit_comment'),
    url(r'^comment/delete/(?P<id>\d+)$',
        views.delete_comment, name='delete_comment'),
    # grading related
    url(r'^grading/apply$', views.apply_grading, name='apply_grading'),
    # others (index: name='index')
    url(r'^error/$', views.error, name='error'),
]
