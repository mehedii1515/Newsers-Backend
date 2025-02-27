from django.contrib import admin

from .models import Article, Category, Rating

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ["name"] }

admin.site.register(Article)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Rating)
