from django.contrib import admin
from .models import Category, Tour, CartItem, Review, FAQ, Favorite, Payment, Profile


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'slug']
    list_display_links = ['pk', 'name']
    search_fields = ['name']
    ordering = ['pk']
    prepopulated_fields = {'slug': ['name']}
    list_per_page = 10


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title']
    list_display_links = ['pk', 'title']
    search_fields = ['title', 'country']
    ordering = ['pk']
    list_filter = ['category', 'country']
    list_per_page = 10


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'tour', 'quantity', 'added_at']
    list_display_links = ['pk', 'user']
    search_fields = ['user__username', 'tour__title']
    ordering = ['-added_at']
    list_per_page = 10


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'tour', 'created_at']
    list_display_links = ['pk', 'user']
    search_fields = ['user__username', 'tour__title']
    ordering = ['-created_at']
    list_per_page = 10


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'tour', 'created_at']
    list_display_links = ['pk', 'user']
    search_fields = ['user__username', 'tour__title']
    ordering = ['-created_at']
    list_per_page = 10


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['pk', 'question']
    list_display_links = ['pk', 'question']
    search_fields = ['question']
    ordering = ['pk']
    list_per_page = 10


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'tour', 'amount', 'status', 'created_at']
    list_display_links = ['pk', 'user']
    search_fields = ['user__username', 'tour__title']
    ordering = ['-created_at']
    list_per_page = 10


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'fio', 'age', 'married', 'license']
    search_fields = ['user__username', 'fio']
    list_filter = ['married', 'license']
