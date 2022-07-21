from django.contrib import admin
from .models import *


class ListingsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "picture", "price", "description", "category", "active")


class BidsAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "price", "listing")

# Register your models here.
admin.site.register(Listings, ListingsAdmin)
admin.site.register(User)
admin.site.register(Bid, BidsAdmin)
admin.site.register(Watchlist)
admin.site.register(Comment)