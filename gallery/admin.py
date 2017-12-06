from django.contrib import admin

# Register your models here.

from .models import Profile, Picture, Comment

admin.site.register(Profile)
admin.site.register(Comment)

@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
	list_display = ('id', 'profile', 'date')