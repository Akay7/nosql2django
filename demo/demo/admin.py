from django.contrib import admin

from .models import Post, User, Tag


class TagInLine(admin.TabularInline):
    model = Tag
    extra = 0


class UserInLine(admin.TabularInline):
    model = User
    extra = 0


class PostAdmin(admin.ModelAdmin):
    inlines = (UserInLine, TagInLine,)
admin.site.register(Post, PostAdmin)
