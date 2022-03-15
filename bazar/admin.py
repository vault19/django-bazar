from django.contrib import admin
from bazar.models import Listing, Profile, City, Category

admin.site.register(Profile)


class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'city', 'category']

admin.site.register(Listing, ListingAdmin)


class CityAdmin(admin.ModelAdmin):
    list_display = ['city']

admin.site.register(City)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'parent', 'name']

admin.site.register(Category, CategoryAdmin)
