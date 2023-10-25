from django.contrib import admin
from .models import *

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'created_at', 'updated_at']
    list_filter = ['author', 'category', 'tags', 'status']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ['-created_at']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'total_post']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

    def total_post(self, obj):
        return obj.post_set.count()


class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
