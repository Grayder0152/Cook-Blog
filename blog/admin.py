from . import models

from django.contrib import admin
from mptt.admin import MPTTModelAdmin


class RecipeInline(admin.StackedInline):
    model = models.Recipe
    extra = 1


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'create_at', 'id')
    prepopulated_fields = {'slug': ('title',)}

    inlines = [RecipeInline]
    save_as = True
    save_on_top = True


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'prep_time', 'cook_time', 'post')


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'website', 'create_at', 'id')


@admin.register(models.Category)
class CategoryAdmin(MPTTModelAdmin, admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_display_links = ('name',)


@admin.register(models.Tag)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_display_links = ('name',)


@admin.register(models.SubscribeEmail)
class SubscribeEmailAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')
