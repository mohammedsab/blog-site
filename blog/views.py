from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import send_mail
from django.conf import settings

from .models import Post
from .forms import EmailPostForm

# Create your views here.


def post_list(request):
    posts = Post.published.all()

    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/post/list.html', {'posts': posts, 'page_obj': page_obj})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post, slug=post,
        status='published',
        publish__year=year,
        publish__month=month,
        publish__day=day)

    return render(request, 'blog/post/detail.html', {'post': post})


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    send = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.changed_data
            # ... send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n\n" \
                f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, settings.EMAIL_HOST_USER,
                      [cd['to']], fail_silently=False)
            send = True

    else:
        form = EmailPostForm()

    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'send': send})
