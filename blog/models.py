from django.db import models

# Create your models here.

from django.db import models
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from .managers import PublishedManager


class Post(models.Model):
    """
    Define a Post class.
    """
    STATUS_CODE = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts') # many-to-one relationship. Define on `many` side.
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CODE,
                              default='draft')
    # default and custom managers
    objects = models.Manager()
    published = PublishedManager()
    # tagging
    tags = TaggableManager()

    class Meta:
        ordering = ('-publish',) # Sort posts by publish date in descending order.

    def __str__(self):
        return "<Post %s>" % self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments')

    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f"<Comment by {self.name} on {self.post}"
