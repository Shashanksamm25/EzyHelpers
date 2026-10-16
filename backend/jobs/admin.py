
from django.contrib import admin
from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "assigned_to",
        "status",
        "created_at",
    )

    list_display_links = ("title",)

    list_filter = ("status",)
    search_fields = ("title", "description", "assigned_to__username")
