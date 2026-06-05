from django.shortcuts import get_object_or_404, render

from ..models import Room

def index(request):
    featured_rooms = (
        Room.objects
        .filter(is_active=True)
        .prefetch_related('images')
        [:3]
    )

    return render(
        request,
        "index.html",
        {
            "featured_rooms":featured_rooms,
        },
    )


def room_list(request):
    rooms = (
        Room.objects
        .filter(is_active=True)
        .prefetch_related("images")
    )
    
    return render(
        request,
        "core/room_list.html",
        {
            "rooms": rooms,
        }
    )


def room_detail(request, slug):
    room = get_object_or_404(
        Room.objects.prefetch_related(
            "images",
            "amenities",
        ),
        slug=slug,
    )

    return render(
        request,
        "core/room_detail.html",
        {
            "room": room,
        }
    )