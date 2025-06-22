from django.contrib import admin
from .models import Seller, Buyer, RealEstate, DKPTemplate, GeneratedDKP


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'passport_series', 'passport_number', 'is_individual')
    search_fields = ('full_name',)
    list_filter = ('is_individual',)


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone')
    search_fields = ('full_name', 'phone')


@admin.register(RealEstate)
class RealEstateAdmin(admin.ModelAdmin):
    list_display = ('get_property_type', 'address', 'area')
    search_fields = ('address', 'cadastral_number')

    def get_property_type(self, obj):
        return dict(RealEstate.PROPERTY_TYPES).get(obj.property_type, 'Unknown')

    get_property_type.short_description = 'Тип объекта'


@admin.register(DKPTemplate)
class DKPTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'doc_type')
    list_filter = ('doc_type',)


@admin.register(GeneratedDKP)
class GeneratedDKPAdmin(admin.ModelAdmin):
    list_display = ('id', 'seller', 'buyer', 'real_estate', 'price', 'created_at')
    readonly_fields = ('created_at', 'price_in_words')
    list_filter = ('template',)