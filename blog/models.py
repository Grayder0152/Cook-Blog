from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.mail import send_mail
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField

User = get_user_model()


class Category(MPTTModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100)
    parent = TreeForeignKey('self', related_name='children', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = 'Categories'


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, unique=True)
    image = models.ImageField(upload_to='articles/')
    mini_text = RichTextField(help_text='This text will display in preview.', default='')
    text = RichTextField(help_text='This is main text will display in detail view page.', unique=True)
    category = models.ManyToManyField(Category, related_name='posts')
    tags = models.ManyToManyField(Tag, related_name='posts')
    create_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=250, unique=True)

    def __str__(self):
        return self.title

    def _do_insert(self, *args, **kwargs):
        result = super()._do_insert(*args, **kwargs)
        subscribe_emails = SubscribeEmail.objects.all()
        send_mail(
            'New post',
            'Was create a new post!!!',
            settings.EMAIL_HOST_USER,
            subscribe_emails,
            fail_silently=False,
        )
        return result

    def get_recipes(self):
        return self.recipes.all()

    def get_absolute_url(self):
        return reverse('post_single', kwargs={'post_slug': self.slug})


class Recipe(models.Model):
    name = models.CharField(max_length=100, unique=True)
    servers = models.CharField(max_length=50)
    prep_time = models.PositiveIntegerField(default=0)
    cook_time = models.PositiveIntegerField(default=0)
    ingredients = RichTextField()
    directions = RichTextField()
    post = models.ForeignKey(Post, related_name='recipes', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    website = models.CharField(max_length=150, blank=True, null=True)
    message = models.TextField(max_length=500)
    create_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, related_name='comment', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class SubscribeEmail(models.Model):
    email = models.EmailField(max_length=150, unique=True)

    def __str__(self):
        return self.email
