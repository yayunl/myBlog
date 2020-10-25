from django.urls import include, path
from .views import PostListView, PostDetailView

urlpatterns = [
    path('', PostListView.as_view(), 'post_list'),
    path('<slug>/detail', PostDetailView.as_view(), 'post_detail')
]