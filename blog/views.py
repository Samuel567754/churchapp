from django.shortcuts import render
# blog/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from .models import Post, Category, Tag, Comment, Like
from .forms import PostForm, CommentForm


def blog(request):
    """
    Display a paginated list of published blog posts along with categories and tags.
    """
    # Fetch published posts, ordered by most recent publication date
    posts = Post.objects.filter(is_published=True).order_by('-published_at').select_related('author').prefetch_related('categories', 'tags')
    
    # Fetch all categories and tags for sidebar or filtering purposes
    categories = Category.objects.all()
    tags = Tag.objects.all()
    featured_post = posts.first()  # Get the first post as featured

    # Set up pagination: 10 posts per page
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page', 1)  # Default to page 1 if 'page' parameter is not provided

    try:
        paginated_posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page.
        paginated_posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page of results.
        paginated_posts = paginator.page(paginator.num_pages)

    context = {
        'posts': paginated_posts,
        'categories': categories,
        'featured_post':featured_post,
        'tags': tags,
        'current_page': paginated_posts.number,
        'total_pages': paginator.num_pages,
    }

    return render(request, 'blog/blog.html', context)

def post_details(request, slug):
    """
    Display a single post with comments and like functionality
    """
    post = get_object_or_404(Post, slug=slug, is_published=True)
    
    # Increment views count
    post.views_count += 1
    post.save()

    # Comments
    comments = post.comments.filter(is_approved=True)
    
    # Like status
    user_liked = False
    if request.user.is_authenticated:
        user_liked = Like.objects.filter(post=post, user=request.user).exists()

    # Comment form
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            messages.success(request, 'Your comment is awaiting approval.')
            return redirect('blog:post_details', slug=post.slug)
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'user_liked': user_liked
    }
    return render(request, 'blog/post_details.html', context)

def category_posts(request, slug):
    """
    List posts for a specific category
    """
    category = get_object_or_404(Category, slug=slug)
    posts = category.posts.filter(is_published=True).order_by('-published_at')
    
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'category': category,
        'posts': posts
    }
    return render(request, 'blog/category_posts.html', context)

def tag_posts(request, slug):
    """
    List posts for a specific tag
    """
    tag = get_object_or_404(Tag, slug=slug)
    posts = tag.posts.filter(is_published=True).order_by('-published_at')
    
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'tag': tag,
        'posts': posts
    }
    return render(request, 'blog/tag_posts.html', context)

@login_required
def like_post(request, slug):
    """
    Like/Unlike functionality for authenticated users
    """
    post = get_object_or_404(Post, slug=slug, is_published=True)
    
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    
    if not created:
        # If like already exists, it means user wants to unlike
        like.delete()
        messages.info(request, 'Post unliked.')
    else:
        messages.success(request, 'Post liked.')
    
    return redirect('blog:post_detail', slug=post.slug)

# @login_required
# def create_post(request):
#     """
#     Create a new blog post
#     """
#     if request.method == 'POST':
#         form = PostForm(request.POST, request.FILES)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.save()
#             form.save_m2m()  # Save many-to-many relationships
#             messages.success(request, 'Post created successfully.')
#             return redirect('blog:post_detail', slug=post.slug)
#     else:
#         form = PostForm()
    
#     return render(request, 'blog/create_post.html', {'form': form})

# @login_required
# def edit_post(request, slug):
#     """
#     Edit an existing blog post
#     """
#     post = get_object_or_404(Post, slug=slug, author=request.user)
    
#     if request.method == 'POST':
#         form = PostForm(request.POST, request.FILES, instance=post)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Post updated successfully.')
#             return redirect('blog:post_detail', slug=post.slug)
#     else:
#         form = PostForm(instance=post)
    
#     return render(request, 'blog/edit_post.html', {'form': form, 'post': post})