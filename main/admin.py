from django.contrib import admin
from unfold.admin import ModelAdmin
from django.contrib.admin.helpers import ActionForm
from django.contrib.auth.models import User
from . import models




admin.site.unregister(User)
@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name', 'email', 'is_staff']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    list_filter = ['is_staff']
    ordering = ['id']
    readonly_fields = ['created_at', 'updated_at']
    


@admin.register(models.Category)
class CategoryAdmin(ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    ordering = ['id']
    readonly_fields = ['created_at', 'updated_at']
    

@admin.register(models.Student)
class StudentAdmin(ModelAdmin):
    list_display = ['id', 'full_name', 'user_id', 'first_p', 'second_p', 'third_p', 'total_p']
    list_display_links = ['full_name', 'user_id']
    search_fields = ['full_name', 'user_id']
    list_filter = ['cats']
    ordering = ['-total_p', '-first_p', '-second_p', '-third_p']
    readonly_fields = ['created_at', 'updated_at', 'total_p', 'first_p', 'second_p', 'third_p']

@admin.action(description="Delete selected objects")
def delete_multi(modeladmin, request, queryset):
    queryset.delete()

admin.site.disable_action("delete_selected")

@admin.register(models.Result)
class ResultAdmin(ModelAdmin):
    list_display = ['id', 'title', 'category', 'date', 'first_place', 'second_place', 'third_place']
    list_display_links = ['title', 'category', 'date']
    list_filter = ['date', 'category', 'created_at']
    
    ordering = ['created_at', 'updated_at', '-date']
    readonly_fields = ['created_at', 'updated_at']
    actions = ['custom_delete']

    def custom_delete(self, request, queryset):
        # Perform custom actions before deletion
        print("Deleting objects:", queryset)

        # Call the model's delete method on each selected object
        for obj in queryset:
            obj.delete()

        # Perform custom actions after deletion
        print("Objects deleted:", queryset)

    custom_delete.short_description = "Custom Delete selected objects"
    custom_delete.form = ActionForm

