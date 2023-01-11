from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Count

from django.contrib.postgres.search import SearchVector
from taggit.models import Tag

from .models import Post, Comments
from .forms import EmailPostForm, CommentForm, SearchForm

# Create your views here.


def post_list(request, tag_slug=None):
    posts = Post.published.all()
    tag = None

    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            posts = Post.published.annotate(
                search=SearchVector('title', 'body'),
            ).filter(search=query)

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])

    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/post/list.html',
                  {'posts': posts, 'page_obj': page_obj, 'tag': tag, 'query': query, })


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post, slug=post,
        status='published',
        publish__year=year,
        publish__month=month,
        publish__day=day)

    # List of active comments for this post
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()

    else:
        comment_form = CommentForm()

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(
        tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count(
        'tags')).order_by('-same_tags', '-publish')[:4]

    return render(request, 'blog/post/detail.html',
                  {'post': post, 'comments': comments,
                   'new_comment': new_comment, 'comment_form': comment_form,
                   'similar_posts': similar_posts})


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    send = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            # ... send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n\n" \
                f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [cd['to']],
            )
            send = True

    else:
        form = EmailPostForm()

    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'send': send})


# def post_search(request):
#     form = SearchForm()
#     query = None
#     results = []

#     if 'query' in request.GET:
#         form = SearchForm(request.GET)
#         if form.is_valid():
#             query = form.cleaned_data['query']
#             results = Post.published.annotate(
#                 search=SearchVector('title', 'body'),
#             ).filter(search=query)

#     return render(request, 'blog/post/list.html',
#                   {
#                       'form': form,
#                       'query': query,
#                       'results': results,
#                   })
