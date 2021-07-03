from blog.models import Category
from django.db import models
from ckeditor.fields import RichTextField


class CategoryItem(models.Model):
    category = models.OneToOneField(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='categories/')

    def __str__(self):
        return self.category.name


class SocialNetwork(models.Model):
    icon = models.FileField(upload_to='icons/')
    name = models.CharField(max_length=200)
    link = models.URLField()

    def __str__(self):
        return self.name


class AboutPage(models.Model):
    name = models.CharField(max_length=50, help_text="Enter your name")
    text = RichTextField()
    mini_text = RichTextField()
    mini_img = models.ImageField(upload_to='about/')
    social_networks = models.ManyToManyField(SocialNetwork, help_text="Chose your social networks")

    def __str__(self):
        return self.name

    def get_images(self):
        return self.about_images.all()


class AboutImage(models.Model):
    image = models.ImageField(upload_to='about/')
    page = models.ForeignKey(AboutPage, on_delete=models.CASCADE, related_name='about_images')
