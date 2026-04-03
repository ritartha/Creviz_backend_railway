from django.contrib import admin

from .models import Project, ProjectTool


class ProjectToolInline(admin.TabularInline):
    model = ProjectTool
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display   = [
        "title", "category", "gradient", "order", "is_visible", "created_at"]
    list_filter    = ["category", "is_visible", "gradient"]
    search_fields  = ["title", "description"]
    list_editable  = ["order", "is_visible"]
    ordering       = ["order"]
    inlines        = [ProjectToolInline]