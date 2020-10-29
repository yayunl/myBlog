from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
from django.views.generic import ListView, CreateView, DetailView
from django.db.models import Count
from taggit.models import Tag
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


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/post/comment_form.html'
    context_object_name = 'comment_form'

    def form_valid(self, form):
        post_slug = self.request.path.split('/')[-2]
        post = Post.objects.filter(slug=post_slug).first()
        form.cleaned_data['post'] = post
        form.save()
        return HttpResponseRedirect(post.get_absolute_url())


class PostListView(ListView):

    context_object_name = 'posts'
    paginate_by = 2
    template_name = 'blog/post/list.html'

    def get_queryset(self,  **kwargs):
        queryset = Post.published.all()  # default object is published post
        tag_slug = self.kwargs.get('tag_slug')
        if tag_slug:
            # Return posts with tags
            tags = get_object_or_404(Tag, slug=tag_slug)
            queryset = queryset.filter(tags__in=[tags])
        return queryset


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post/detail.html'

    def post(self, request, **kwargs):
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            current_post = Post.objects.filter(slug=kwargs.get('slug')).first()
            new_comment.post = current_post
            # actual save
            new_comment.save()
            # return rendered context
            self.object = self.get_object()
            context = self.get_context_data()
            return super(DetailView, self).render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = context.get('object') # get the post
        # Get active comments for this post
        comments = obj.comments.filter(active=True)
        context['comments'] = comments
        context['total_comments'] = comments.count()
        # Pass an empty comment form
        context['form'] = CommentForm()
        return context

