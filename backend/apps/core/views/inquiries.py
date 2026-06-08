import logging

from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from ..forms import InquiryForm
from ..models import Inquiry, PropertyInfo

logger = logging.getLogger(__name__)


@require_http_methods(["GET", "POST"])
def inquiry_create(request, room_slug=None):
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
                inquiry.full_name,
                inquiry.email,
                inquiry.room,
                inquiry.date_from,
                inquiry.date_to,
            )
            _send_inquiry_confirmation(inquiry)

            if request.headers.get("HX-Request"):
                return render(request, "core/_inquiry_success.html",
                              {"inquiry": inquiry})

            messages.success(request, "Twoje zapytanie zostało wysłane!")
            return redirect("inquiry-create")

        else:
            logger.warning("Nieprawidłowy formularz: %s", form.errors.as_json())
            if request.headers.get("HX-Request"):
                return render(request, "core/_inquiry_form.html", {"form": form})

    else:
        form = InquiryForm(initial=initial)

    return render(request, "core/inquiry_form.html", {"form": form})


def contact(request):
    cache_key = "property_info_contact"
    prop = cache.get(cache_key)
    if prop is None:
        prop = PropertyInfo.objects.first()
        cache.set(cache_key, prop, timeout=60 * 15)
        logger.debug("PropertyInfo załadowane z bazy")
    return render(request, "core/contact.html", {"prop": prop})


@cache_page(60 * 30)
def property_info(request):
    prop = PropertyInfo.objects.first()
    return render(request, "core/property_info.html", {"prop": prop})


@login_required(login_url="login")
def inquiry_list(request):
    inquiries = Inquiry.objects.select_related("room").order_by("-created_at")
    logger.info(
        "Użytkownik '%s' wyświetlił listę zapytań (%d rekordów)",
        request.user.username,
        inquiries.count(),
    )
    return render(request, "core/inquiry_list.html", {"inquiries": inquiries})


def _send_inquiry_confirmation(inquiry):
    subject = f"[U Alchemika] Potwierdzenie zapytania #{inquiry.pk}"
    body = render_to_string("core/emails/inquiry_confirmation.txt",
                            {"inquiry": inquiry})
    try:
        send_mail(
            subject=subject,
            message=body,
            from_email="noreply@u-alchemika.pl",
            recipient_list=[inquiry.email],
            fail_silently=False,
        )
        logger.info("E-mail wysłany na %s", inquiry.email)
    except Exception as exc:
        logger.error("Błąd wysyłki e-maila dla zapytania #%d: %s", inquiry.pk, exc)
