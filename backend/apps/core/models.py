from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class Amenity(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = 'Udogodnienie'
        verbose_name_plural = 'Udogodnienia'

    def __str__(self):
        return self.name


class Room(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    capacity = models.PositiveIntegerField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    amenities = models.ManyToManyField(Amenity, through='RoomAmenity', blank=True)

    class Meta:
        verbose_name = 'Pokój'
        verbose_name_plural = 'Pokoje'
        indexes = [models.Index(fields=['slug'], name='room_slug_idx')]

    def __str__(self):
        return self.name


class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='images')
    image_url = models.TextField()
    alt_text = models.CharField(max_length=255, blank=True)
    display_order = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Zdjęcie pokoju'
        verbose_name_plural = 'Zdjęcia pokoi'
        ordering = ['display_order']

    def __str__(self):
        return f'{self.room.name} – zdjęcie {self.display_order}'


class RoomAmenity(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['room', 'amenity']]
        verbose_name = 'Udogodnienie pokoju'
        verbose_name_plural = 'Udogodnienia pokoi'

    def __str__(self):
        return f'{self.room.name} – {self.amenity.name}'


class Inquiry(models.Model):
    STATUS_NEW = 'new'
    STATUS_REPLIED = 'replied'
    STATUS_CLOSED = 'closed'
    STATUS_CHOICES = [
        (STATUS_NEW, 'Nowe'),
        (STATUS_REPLIED, 'Odpowiedziano'),
        (STATUS_CLOSED, 'Zamknięte'),
    ]

    room = models.ForeignKey(Room, null=True, blank=True, on_delete=models.SET_NULL)
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    date_from = models.DateField(null=True, blank=True)
    date_to = models.DateField(null=True, blank=True)
    guests = models.PositiveIntegerField(null=True, blank=True)
    message = models.TextField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=STATUS_NEW)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Zapytanie'
        verbose_name_plural = 'Zapytania'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status'], name='inquiry_status_idx'),
            models.Index(fields=['email'], name='inquiry_email_idx'),
            models.Index(fields=['created_at'], name='inquiry_created_at_idx'),
        ]

    def clean(self):
        if self.date_from and self.date_to and self.date_to < self.date_from:
            raise ValidationError('Data wyjazdu musi być późniejsza niż data przyjazdu.')

    def __str__(self):
        return f'{self.full_name} ({self.get_status_display()})'


class AuditLog(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    action = models.CharField(max_length=100)
    entity_name = models.CharField(max_length=100)
    entity_id = models.BigIntegerField(null=True)
    details = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Log audytu'
        verbose_name_plural = 'Logi audytu'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.action} / {self.entity_name} #{self.entity_id}'
