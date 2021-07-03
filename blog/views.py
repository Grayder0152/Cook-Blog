from .models import Post, Comment, SubscribeEmail
from .forms import CommentForm, EmailSubscribeForm

from content.models import CategoryItem
from django.views.generic import ListView, DetailView, CreateView
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def handler404(request, exception=None):
    return render(request, '404.html')


def post_paginator(instance, post_list):
    page = instance.request.GET.get('page', 1)
    paginator = Paginator(post_list, instance.paginate_by)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return posts, paginator


class HomeView(ListView):
    model = Post
    template_name = 'blog/home.html'

    def get_queryset(self):
        return Post.objects.order_by('id').prefetch_related('category').prefetch_related('comment').select_related(
            'author')[:5]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_item'] = CategoryItem.objects.all().prefetch_related('category__posts')[:4]
        return context

    def get(self, request, *args, **kwargs):
        last_post_id = request.GET.get('lastPostId')
        if last_post_id is not None:
            more_posts = Post.objects.filter(id__gt=int(last_post_id))
            if not more_posts:
                return JsonResponse({'data': False})

            data = []
            for post in more_posts[:4]:
                obj = {
                    'id': post.id,
                    'title': post.title,
                    'author': post.author.username,
                    'image_url': post.image.url,
                    'mini_text': post.mini_text[:200] + '...',
                    'category': ', '.join(i.name for i in post.category.all()),
                    'create_at_day': str(post.create_at.strftime('%-d')),
                    'create_at_month': str(post.create_at.strftime('%b')),
                    'url': str(post.get_absolute_url()),
                    'count_comment': str(post.comment.count()),
                    'last_id': more_posts.order_by('id').last().id
                }
                data.append(obj)
            data[-1]['last_post'] = True
            return JsonResponse({'data': data})
        return super().get(request, *args, **kwargs)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'

    def get_object(self, queryset=None):
        posts = Post.objects.all().prefetch_related('comment')
        return posts.get(slug=self.kwargs.get(self.slug_url_kwarg))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        context['category_name'] = str(slug).title()

        post_list = Post.objects.filter(category__slug=slug).prefetch_related('category').prefetch_related('comment').select_related('author')
        context['post_list'], context['paginator'] = post_paginator(self, post_list)
        return context


class SearchPostView(ListView):
    model = Post
    template_name = 'blog/search_post.html'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')

        post_list = Post.objects.filter(title__icontains=context['q']).prefetch_related('category').prefetch_related(
            'comment').select_related('author')
        context['post_list'], context['paginator'] = post_paginator(self, post_list)
        return context


class CreateComment(CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        self.success_url = self.request.META.get('HTTP_REFERER')
        form.instance.post_id = self.kwargs.get('pk')
        self.object = form.save()
        return super().form_valid(form)


class AddEmailSubscribe(CreateView):
    model = SubscribeEmail
    form_class = EmailSubscribeForm

    def post(self, request, *args, **kwargs):
        form = EmailSubscribeForm(request.POST)
        self.success_url = self.request.META.get('HTTP_REFERER')
        if form.is_valid():
            form.save()
            messages.add_message(self.request, messages.INFO, f'Your email was add in list.')
        else:
            messages.add_message(self.request, messages.ERROR, f'Your email already exit in list.')
        return HttpResponseRedirect(self.success_url)
