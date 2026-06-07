"""
Widoki Osoby B: zapytania, kontakt, informacje o obiekcie.

Pokrycie zagadnień:
  #1  MVC — widoki Django (V w MVT)
  #4  cache — @cache_page na property_info + ręczny cache na contact
  #9  routing — name= w urls.py, reverse_lazy
  #10 ORM — form.save() przez Django ORM
  #11 uwierzytelnianie — @login_required na inquiry_list
  #13 mailing — send_mail po zapisaniu zapytania
  #14 formularze — InquiryForm (ModelForm)
  #15 async HTMX — zwrot partiali bez przeładowania strony
  #19 logger — logowanie zapytań i błędów
"""

import logging

from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods

from ..forms import InquiryForm
from ..models import Inquiry, PropertyInfo

# Zagadnienie #19 — logger
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Formularz zapytań — HTMX
# Zagadnienia: #14 formularze, #15 async HTMX, #10 ORM, #13 mailing, #19 logger
# ---------------------------------------------------------------------------

@require_http_methods(["GET", "POST"])
def inquiry_create(request, room_slug=None):
    """
    GET  → pełna strona z formularzem
    POST via HTMX → zwraca partial z formularzem (błędy) lub partial sukcesu
    """
    initial = {}
    if room_slug:
        from ..models import Room
        room = get_object_or_404(Room, slug=room_slug)
        initial["room"] = room

    if request.method == "POST":
        form = InquiryForm(request.POST, initial=initial)

        if form.is_valid():
            inquiry = form.save()
            logger.info(
                "Nowe zapytanie #%d od %s <%s> na pokój '%s' (%s–%s)",
                inquiry.pk,
                inquiry.guest_name,
                inquiry.guest_email,
                inquiry.room,
                inquiry.check_in,
                inquiry.check_out,
            )

            # Zagadnienie #13 — mailing
            _send_inquiry_confirmation(inquiry)

            # Zagadnienie #15 — HTMX: zwrot partial sukcesu
            if request.headers.get("HX-Request"):
                return render(request, "core/_inquiry_success.html",
                              {"inquiry": inquiry})

            # fallback bez HTMX
            from django.contrib import messages
            messages.success(request,
                             "Twoje zapytanie zostało wysłane! Odpiszemy wkrótce.")
            from django.shortcuts import redirect
            return redirect("inquiry-create")

        else:
            logger.warning(
                "Nieprawidłowy formularz zapytania: %s", form.errors.as_json()
            )
            # Zagadnienie #15 — HTMX: zwrot partial z błędami
            if request.headers.get("HX-Request"):
                return render(request, "core/_inquiry_form.html", {"form": form})

    else:
        form = InquiryForm(initial=initial)

    return render(request, "core/inquiry_form.html", {"form": form})


# ---------------------------------------------------------------------------
# Strona kontaktu
# Zagadnienia: #4 cache (ręczny), #1 MVC
# ---------------------------------------------------------------------------

def contact(request):
    """
    Dane kontaktowe obiektu.
    PropertyInfo jest rzadko zmieniana — cache 15 minut.
    """
    cache_key = "property_info_contact"
    prop = cache.get(cache_key)
    if prop is None:
        prop = PropertyInfo.objects.first()
        cache.set(cache_key, prop, timeout=60 * 15)
        logger.debug("PropertyInfo załadowane z bazy, klucz cache: %s", cache_key)
    else:
        logger.debug("PropertyInfo pobrane z cache, klucz: %s", cache_key)

    return render(request, "core/contact.html", {"prop": prop})


# ---------------------------------------------------------------------------
# Informacje o obiekcie
# Zagadnienia: #4 cache (dekorator @cache_page)
# ---------------------------------------------------------------------------

@cache_page(60 * 30)   # 30 minut — dane rzadko się zmieniają
def property_info(request):
    """
    Godziny, płatności, polityki, regulamin — pobrane z PropertyInfo.
    Zagadnienie #4: @cache_page cachuje całą odpowiedź HTTP.
    """
    prop = PropertyInfo.objects.first()
    return render(request, "core/property_info.html", {"prop": prop})


# ---------------------------------------------------------------------------
# Lista zapytań (tylko dla zalogowanych)
# Zagadnienie #11 — uwierzytelnianie
# ---------------------------------------------------------------------------

@login_required(login_url="login")
def inquiry_list(request):
    """
    Widok panelowy — lista wszystkich zapytań dla zalogowanego personelu.
    Dostęp chroniony przez @login_required (zagadnienie #11).
    """
    inquiries = (
        Inquiry.objects.select_related("room")
        .order_by("-created_at")
    )
    logger.info(
        "Użytkownik '%s' wyświetlił listę zapytań (%d rekordów)",
        request.user.username,
        inquiries.count(),
    )
    return render(request, "core/inquiry_list.html", {"inquiries": inquiries})


# ---------------------------------------------------------------------------
# Helpery
# ---------------------------------------------------------------------------

def _send_inquiry_confirmation(inquiry):
    """
    Zagadnienie #13 — wysyłanie e-maila po przyjęciu zapytania.
    W środowisku dev e-mail trafia do MailHog (patrz docker-compose.yml).
    """
    subject = f"[U Alchemika] Potwierdzenie zapytania #{inquiry.pk}"
    body = render_to_string("core/emails/inquiry_confirmation.txt",
                            {"inquiry": inquiry})
    try:
        send_mail(
            subject=subject,
            message=body,
            from_email="noreply@u-alchemika.pl",
            recipient_list=[inquiry.guest_email],
            fail_silently=False,
        )
        logger.info("E-mail potwierdzający wysłany na %s", inquiry.guest_email)
    except Exception as exc:
        # Nie blokujemy zapisu — logujemy błąd i idziemy dalej
        logger.error(
            "Błąd wysyłki e-maila dla zapytania #%d: %s", inquiry.pk, exc
        )
