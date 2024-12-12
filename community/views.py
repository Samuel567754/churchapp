from django.shortcuts import render
from community.models import CarouselItem
from event.models import GalleryImage
from django.core.paginator import Paginator

def home(request):
    carousel_items = CarouselItem.objects.filter(is_active=True)
    
   # Pagination setup for gallery images
    images_per_page = 3  # Number of images to show per page
    gallery_images = GalleryImage.objects.all()
    paginator = Paginator(gallery_images, images_per_page)
    page_number = request.GET.get('page', 1)  # Current page number
    page_obj = paginator.get_page(page_number)

    context = {
        'carousel_items': carousel_items,
        'gallery_images': page_obj.object_list,  # Current page of images
        'has_next': page_obj.has_next(),  # Check if more pages exist
        'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
    }
    return render(request, 'community/home.html', context)


def about(request):
    return render(request, 'community/about.html')

def events(request):
    return render(request, 'community/events.html')

def services(request):
    return render(request, 'community/services.html')

def give(request):
    return render(request, 'community/give.html')

def contact(request):
    return render(request, 'community/contact.html')

def ministries(request):
    return render(request, 'community/ministries.html')






