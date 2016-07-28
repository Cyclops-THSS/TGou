from django.contrib import admin
from .models import *


@admin.register(ShopCategory)
class SCAdmin(admin.ModelAdmin):
    pass


@admin.register(CommodityCategory)
class CCAdmin(admin.ModelAdmin):
    pass
