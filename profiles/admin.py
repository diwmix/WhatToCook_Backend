from django.contrib import admin
from .models import CustomUser, Rating

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'age', 'average_rating')
    search_fields = ('username', 'email')
    list_filter = ('age', 'average_rating')
    actions = ['reset_average_rating']

    def reset_average_rating(self, request, queryset):
        for user in queryset:
            user.update_average_rating()
    reset_average_rating.short_description = 'Скинути середній рейтинг для обраних користувачів'

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'rated_by', 'rating')
    search_fields = ('user__username', 'rated_by__username')
    list_filter = ('rating',)
    raw_id_fields = ('user', 'rated_by')
    actions = ['remove_ratings']

    def remove_ratings(self, request, queryset):
        for rating in queryset:
            rating.user.update_average_rating()
            rating.delete()
    remove_ratings.short_description = 'Видалити обрані оцінки'
