from .models import Attraction

def attractions_teaser(request):
    attractions = Attraction.objects.all()[:5]  # Pobierz 5 pierwszych atrakcji
    return {'attractions_teaser': attractions.all()[:3],
    }

