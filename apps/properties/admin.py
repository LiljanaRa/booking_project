from django.contrib import admin
from apps.properties.models.property import Property
from apps.properties.models.address import Address
from apps.properties.models.review import Review


class AddressInline(admin.StackedInline):
    model = Address
    extra = 1


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    inlines = [AddressInline]
    list_display = (
        'title',
        'owner',
        'property_type',
        'price_per_night',
        'is_active',
        'created_at'
    )
    list_filter = (
        'property_type',
        'is_active'
    )
    search_fields = (
        'title',
        'description',
        'owner__email',
        'address__city'
    )
    ordering = ('-created_at',)
    autocomplete_fields = ('owner',)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        'city',
        'street',
        'zip_code',
        'country'
    )
    search_fields = (
        'city',
        'street',
        'zip_code'
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'property',
        'author',
        'comment',
        'rating',
        'created_at'
    )
    list_filter = (
        'rating',
        'created_at'
    )
    search_fields = (
        'property__title',
        'author__email',
        'comment'
    )
    ordering = (
        '-rating',
        'created_at'
    )