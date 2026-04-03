from django.contrib import admin

from .models import Commission


@admin.register(Commission)
class CommissionAdmin(admin.ModelAdmin):
    list_display    = [
        "full_name", "email", "commission_type",
        "budget", "status", "created_at",
    ]
    list_filter     = ["status", "commission_type"]
    search_fields   = ["full_name", "email"]
    list_editable   = ["status"]
    readonly_fields = ["created_at", "updated_at"]
    fieldsets       = [
        ("Client",  {"fields": ["full_name", "email"]}),
        ("Request", {"fields": [
            "commission_type", "budget", "deadline",
            "description", "reference_image",
        ]}),
        ("Admin",   {"fields": ["status", "admin_notes"]}),
        ("Dates",   {"fields": ["created_at", "updated_at"]}),
    ]