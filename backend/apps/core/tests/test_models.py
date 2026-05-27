from datetime import date

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.core.models import Amenity, AuditLog, Inquiry, Room, RoomAmenity, RoomImage


class CoreModelIntegrationTests(TestCase):
    def create_room(self):
        return Room.objects.create(
            name='Test room',
            slug='test-room',
            capacity=2,
            base_price='150.00',
        )

    def test_room_delete_cascades_to_images_and_amenities(self):
        room = self.create_room()
        amenity = Amenity.objects.create(name='WiFi')
        RoomImage.objects.create(room=room, image_url='https://example.com/room.jpg')
        RoomAmenity.objects.create(room=room, amenity=amenity)

        room.delete()

        self.assertEqual(RoomImage.objects.count(), 0)
        self.assertEqual(RoomAmenity.objects.count(), 0)
        self.assertEqual(Amenity.objects.count(), 1)

    def test_room_and_user_delete_set_nullable_foreign_keys_to_null(self):
        room = self.create_room()
        user = User.objects.create_user(username='admin')
        inquiry = Inquiry.objects.create(
            room=room,
            full_name='Jan Kowalski',
            email='jan@example.com',
            message='Czy pokoj jest wolny?',
        )
        audit_log = AuditLog.objects.create(
            user=user,
            action='create',
            entity_name='Room',
            entity_id=room.id,
        )

        room.delete()
        user.delete()
        inquiry.refresh_from_db()
        audit_log.refresh_from_db()

        self.assertIsNone(inquiry.room)
        self.assertIsNone(audit_log.user)

    def test_inquiry_rejects_date_to_before_date_from(self):
        inquiry = Inquiry(
            full_name='Anna Nowak',
            email='anna@example.com',
            date_from=date(2026, 8, 10),
            date_to=date(2026, 8, 9),
            guests=2,
            message='Prosze o oferte.',
        )

        with self.assertRaises(ValidationError):
            inquiry.full_clean()
