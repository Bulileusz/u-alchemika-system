from django.contrib import admin

from .models import Amenity, AuditLog, Inquiry, Room, RoomAmenity, RoomImage


class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1


class RoomAmenityInline(admin.TabularInline):
    model = RoomAmenity
    extra = 1


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'capacity', 'base_price', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [RoomImageInline, RoomAmenityInline]


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon']
    search_fields = ['name']


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'status', 'room', 'date_from', 'date_to', 'created_at']
    list_filter = ['status', 'room']
    search_fields = ['full_name', 'email']
    list_editable = ['status']
    readonly_fields = ['created_at']


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['action', 'entity_name', 'entity_id', 'user', 'created_at']
    list_filter = ['action', 'entity_name']
    search_fields = ['action', 'entity_name', 'details']
    readonly_fields = ['created_at']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
