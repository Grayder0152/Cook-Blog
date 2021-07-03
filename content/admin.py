from .models import CategoryItem, AboutPage, AboutImage, SocialNetwork
from django.contrib import admin

admin.site.register(CategoryItem)
admin.site.register(SocialNetwork)


class ImageAboutInline(admin.StackedInline):
    model = AboutImage
    extra = 1


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    inlines = [ImageAboutInline]
