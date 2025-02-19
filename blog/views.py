from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Post, Category
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import NewsletterSubscriber

@require_POST
def subscribe_newsletter(request):
    email = request.POST.get('email')
    category_ids = request.POST.getlist('categories')
    
    if email:
        try:
            subscriber, created = NewsletterSubscriber.objects.get_or_create(
                email=email,
                defaults={'is_active': True}
            )
            
            if category_ids:
                subscriber.categories.set(category_ids)
            
            return JsonResponse({
                'status': 'success',
                'message': 'Thank you for subscribing to our newsletter!'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': 'An error occurred. Please try again.'
            })
    
    return JsonResponse({
        'status': 'error',
        'message': 'Email is required'
    })




def post_list(request):
    posts = Post.objects.all()
    categories = Category.objects.all()
    featured_posts = Post.objects.filter(is_featured=True)[:3]
    
    # Pagination
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'featured_posts': featured_posts,
    }
    return render(request, 'blog/post_list.html', context)

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    related_posts = Post.objects.filter(category=post.category).exclude(id=post.id)[:3]
    
    context = {
        'post': post,
        'related_posts': related_posts,
    }
    return render(request, 'blog/post_detail.html', context)

def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category)
    
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'blog/category_posts.html', context)
