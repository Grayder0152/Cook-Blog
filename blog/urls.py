from . import views
from django.urls import path

urlpatterns = [
    path('search-post/', views.SearchPostView.as_view(), name='search_post'),
    path('comment/<int:pk>/', views.CreateComment.as_view(), name='create_comment'),
    path('email-subscribe/', views.AddEmailSubscribe.as_view(), name='email_subscribe'),
    path('category/<slug:slug>/', views.PostListView.as_view(), name='post_list'),
    path('<slug:post_slug>/', views.PostDetailView.as_view(), name='post_single'),
    path('', views.HomeView.as_view(), name='home'),

]
