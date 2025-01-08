from django.contrib import admin
from .models import Recipe

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'category']
    search_fields = ['title', 'ingredients']
    actions = ['approve_recipes']

    def approve_recipes(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f"{queryset.count()} recipes approved.")
    approve_recipes.short_description = "Approve selected recipes"