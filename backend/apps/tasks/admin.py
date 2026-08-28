from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "status", "priority", "due_date", "user"]
    search_fields = ["name", "description"]
    list_filter = ["status", "priority"]
    readonly_fields = ["user"]

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)
