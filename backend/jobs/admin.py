
from django.contrib import admin
from .models import Job, JobAssignment


class JobAssignmentInline(admin.TabularInline):
    model = JobAssignment
    extra = 1
    autocomplete_fields = ["helper"]
    fields = ("helper", "status", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_at", "updated_at")
    list_display_links = ("title",)
    search_fields = ("title", "description")
    inlines = [JobAssignmentInline]


@admin.register(JobAssignment)
class JobAssignmentAdmin(admin.ModelAdmin):
    list_display = ("id", "job", "helper", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("job__title", "helper__username")
    list_select_related = ("job", "helper")
