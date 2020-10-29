from django.urls import include, path
from .views import PostListView, PostDetailView, CommentCreateView

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('tag/<slug:tag_slug>', PostListView.as_view(), name='post_list_by_tag'),
    path('<slug>/detail', PostDetailView.as_view(), name='post_detail'),
    # path('<post_slug>/new_comment', CommentCreateView.as_view(), name='comment_create')
]