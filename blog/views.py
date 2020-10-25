from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.views.generic import ListView, CreateView, DetailView
# Create your views here.
from .models import Post, Comment
from .forms import CommentForm, EmailPostForm


def post_share(request, post_id):
    # Get the post to be shared by post id
    post = get_object_or_404(Post, id=post_id, status='published')

    sent = False
    if request.method == 'POST':
        # form was submitted. Use the form to render the request.
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            # Send the email
            subject = f"{cd['name']} recommends you read " \
                      f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"

            send_mail(subject, message, 'admin@myblog.com',
                      [cd['to']])
            sent = True
    else:
         # Create a form template
        form = EmailPostForm()

    return render(request, 'blog/post/share.html',
                  {'post': post,
                   'form': form,
                   'sent': sent})


class PostListView(ListView):
    queryset = Post.published.all() # default object is published post
    context_object_name = 'posts'
    pagination_by =3
    template_name = 'blog/post/list.html'


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = context.get('object') # get the post
        # Get active comments for this post
        comments = Post.objects.filter(comments__active=True)
        context['comments'] = comments
        context['total_comments'] = comments.count()

