from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_room_updated_at'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='inquiry',
            index=models.Index(fields=['created_at'], name='inquiry_created_at_idx'),
        ),
    ]
