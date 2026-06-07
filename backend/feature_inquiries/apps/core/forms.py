from django import forms
from django.utils import timezone
from .models import Inquiry


class InquiryForm(forms.ModelForm):
    """
    Formularz zapytania o pokój.
    Walidacja dat pochodzi z modelu (clean_*) oraz z poziomu formularza.
    Zagadnienia: #14 formularze, #10 ORM (ModelForm → zapis przez ORM)
    """

    class Meta:
        model = Inquiry
        fields = ["guest_name", "guest_email", "guest_phone", "room",
                  "check_in", "check_out", "guests_count", "message"]
        widgets = {
            "guest_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Imię i nazwisko",
                "autocomplete": "name",
            }),
            "guest_email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "adres@email.pl",
                "autocomplete": "email",
            }),
            "guest_phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "+48 000 000 000",
                "autocomplete": "tel",
            }),
            "room": forms.Select(attrs={
                "class": "form-select",
            }),
            "check_in": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date",
            }),
            "check_out": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date",
            }),
            "guests_count": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 1,
                "max": 10,
            }),
            "message": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Dodatkowe pytania lub życzenia…",
                "maxlength": 1000,
                "id": "id_message",
            }),
        }
        labels = {
            "guest_name": "Imię i nazwisko",
            "guest_email": "Adres e-mail",
            "guest_phone": "Telefon (opcjonalnie)",
            "room": "Pokój",
            "check_in": "Data przyjazdu",
            "check_out": "Data wyjazdu",
            "guests_count": "Liczba gości",
            "message": "Wiadomość (opcjonalnie)",
        }

    def clean_check_in(self):
        check_in = self.cleaned_data.get("check_in")
        today = timezone.localdate()
        if check_in and check_in < today:
            raise forms.ValidationError("Data przyjazdu nie może być w przeszłości.")
        return check_in

    def clean(self):
        cleaned = super().clean()
        check_in = cleaned.get("check_in")
        check_out = cleaned.get("check_out")

        if check_in and check_out:
            if check_out <= check_in:
                self.add_error("check_out",
                               "Data wyjazdu musi być późniejsza niż data przyjazdu.")
            elif (check_out - check_in).days > 30:
                self.add_error("check_out",
                               "Pobyt nie może trwać dłużej niż 30 dni.")
        return cleaned
