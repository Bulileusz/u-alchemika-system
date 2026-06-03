from .models import PropertyInfo

def property_info(request):
    try:
        info = PropertyInfo.objects.first()
    except Exception:
        info = None
    return {'property_info': info}
    