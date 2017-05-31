from django.contrib import admin

from .models import Post, User, Tag


class UserAdmin(admin.ModelAdmin):
    pass
admin.site.register(User, UserAdmin)


class TagAdmin(admin.ModelAdmin):
    pass
admin.site.register(Tag, TagAdmin)


class PostAdmin(admin.ModelAdmin):
    pass
admin.site.register(Post, PostAdmin)
