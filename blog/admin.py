from django.contrib import admin
from .models import Comments, Post

# Register your models here.

# admin.site.register(Post)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # ('title', 'slug', 'author', 'body', 'publish', 'created', 'updated', 'status', )
    list_display = ('title', 'slug', 'author', 'publish', 'status',)
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    '''Admin View for Comments'''
    # ('post', 'name', 'email', 'body', 'created', 'updated', 'active')
    list_display = ('post', 'name', 'email', 'created', 'active')
    list_filter = ('active', 'created', 'updated',)
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    search_fields = ('name', 'email', 'body')
    date_hierarchy = 'created'
    ordering = ('active',)
