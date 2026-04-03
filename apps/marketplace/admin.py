from django.contrib import admin

from .models import Order, Product, ProductBadge, ProductFormat, ProductSoftware


class ProductBadgeInline(admin.TabularInline):
    model = ProductBadge
    extra = 1


class ProductSoftwareInline(admin.TabularInline):
    model = ProductSoftware
    extra = 1


class ProductFormatInline(admin.TabularInline):
    model = ProductFormat
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display  = [
        "title", "category", "price", "original_price",
        "rating", "downloads", "featured", "is_active", "date_added",
    ]
    list_filter   = ["category", "featured", "is_active"]
    search_fields = ["title", "description"]
    list_editable = ["featured", "is_active"]
    inlines       = [ProductBadgeInline, ProductSoftwareInline, ProductFormatInline]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display    = [
        "id", "product", "full_name", "email",
        "amount", "status", "created_at",
    ]
    list_filter     = ["status"]
    search_fields   = ["full_name", "email", "product__title"]
    readonly_fields = ["created_at", "updated_at"]