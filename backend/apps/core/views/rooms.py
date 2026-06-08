from pathlib import Path

from django.conf import settings
from django.shortcuts import get_object_or_404, render

from ..models import Room

GALLERY_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
GALLERY_EXCLUDED_IMAGE_KEYWORDS = (
    "lawendowy",
    "lesny",
    "izerski",
    "gorski",
    "rodzinny",
    "logo",
    "torn-edge",
)

ROOM_MAIN_IMAGE_STATIC_PATHS = {
    "pokoj-lawendowy": "images/lawendowy.jpeg",
    "pokoj-gorski": "images/gorski.jpg",
    "pokoj-lesny": "images/lesny.jpg",
    "pokoj-izerski": "images/izerski.jpg",
    "apartament-rodzinny": "images/lawendowy.jpeg",
}


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
            "room_main_image_static_path": ROOM_MAIN_IMAGE_STATIC_PATHS.get(room.slug),
        }
    )


def gallery(request):
    images_dir = Path(settings.STATICFILES_DIRS[0]) / "images"
    gallery_images = []

    if images_dir.exists():
        for image_path in sorted(images_dir.iterdir(), key=lambda path: path.name.lower()):
            image_name = image_path.name
            image_name_lower = image_name.lower()

            if image_path.suffix.lower() not in GALLERY_IMAGE_EXTENSIONS:
                continue

            if any(keyword in image_name_lower for keyword in GALLERY_EXCLUDED_IMAGE_KEYWORDS):
                continue

            gallery_images.append(
                {
                    "src": f"images/{image_name}",
                    "alt": "Galeria U Alchemika",
                }
            )

    return render(
        request,
        "core/gallery.html",
        {
            "gallery_images": gallery_images,
        },
    )
