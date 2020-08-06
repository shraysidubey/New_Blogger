from django.contrib import admin
from blogs.models import blog, UserProfile

class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}

admin.site.register(blog, BlogAdmin)
admin.site.register(UserProfile)