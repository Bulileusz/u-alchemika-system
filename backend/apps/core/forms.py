from django import forms
from django.utils import timezone
from .models import Inquiry


class InquiryForm(forms.ModelForm):

    class Meta:
        model = Inquiry
        fields = ["full_name", "email", "phone", "room",
                  "date_from", "date_to", "guests", "message"]
        widgets = {
            "full_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Imię i nazwisko",
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "adres@email.pl",
            }),
            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "+48 000 000 000",
            }),
            "room": forms.Select(attrs={
                "class": "form-select",
            }),
            "date_from": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date",
            }),
            "date_to": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date",
            }),
            "guests": forms.NumberInput(attrs={
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
            "full_name": "Imię i nazwisko",
            "email": "Adres e-mail",
            "phone": "Telefon (opcjonalnie)",
            "room": "Pokój",
            "date_from": "Data przyjazdu",
            "date_to": "Data wyjazdu",
            "guests": "Liczba gości",
            "message": "Wiadomość",
        }

    def clean_date_from(self):
        date_from = self.cleaned_data.get("date_from")
        if date_from and date_from < timezone.localdate():
            raise forms.ValidationError("Data przyjazdu nie może być w przeszłości.")
        return date_from

    def clean(self):
        cleaned = super().clean()
        date_from = cleaned.get("date_from")
        date_to = cleaned.get("date_to")
        if date_from and date_to:
            if date_to <= date_from:
                self.add_error("date_to",
                               "Data wyjazdu musi być późniejsza niż data przyjazdu.")
            elif (date_to - date_from).days > 30:
                self.add_error("date_to",
                               "Pobyt nie może trwać dłużej niż 30 dni.")
        return cleaned