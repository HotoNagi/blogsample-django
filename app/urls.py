from django.urls import path
from app import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # 詳細用のURL
    # pkには投稿のidが入る こうするとどの投稿の詳細なのかを区別することができる
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    # 投稿用のURL
    path('post/new/', views.CreatePostView.as_view(), name='post_new'),
    path('post/<int:pk>/edit', views.PostEditView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete', views.PostDeleteView.as_view(), name='post_delete')
]
