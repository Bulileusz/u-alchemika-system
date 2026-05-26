import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Amenity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('icon', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'verbose_name': 'Udogodnienie',
                'verbose_name_plural': 'Udogodnienia',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('slug', models.SlugField(max_length=150, unique=True)),
                ('description', models.TextField(blank=True)),
                ('capacity', models.PositiveIntegerField()),
                ('base_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Pokój',
                'verbose_name_plural': 'Pokoje',
            },
        ),
        migrations.CreateModel(
            name='RoomImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.TextField()),
                ('alt_text', models.CharField(blank=True, max_length=255)),
                ('display_order', models.IntegerField(default=0)),
                ('room', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='images',
                    to='core.room',
                )),
            ],
            options={
                'verbose_name': 'Zdjęcie pokoju',
                'verbose_name_plural': 'Zdjęcia pokoi',
                'ordering': ['display_order'],
            },
        ),
        migrations.CreateModel(
            name='RoomAmenity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amenity', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='core.amenity',
                )),
                ('room', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='core.room',
                )),
            ],
            options={
                'verbose_name': 'Udogodnienie pokoju',
                'verbose_name_plural': 'Udogodnienia pokoi',
                'unique_together': {('room', 'amenity')},
            },
        ),
        migrations.AddField(
            model_name='room',
            name='amenities',
            field=models.ManyToManyField(blank=True, through='core.RoomAmenity', to='core.amenity'),
        ),
        migrations.CreateModel(
            name='Inquiry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(blank=True, max_length=50)),
                ('date_from', models.DateField(blank=True, null=True)),
                ('date_to', models.DateField(blank=True, null=True)),
                ('guests', models.PositiveIntegerField(blank=True, null=True)),
                ('message', models.TextField()),
                ('status', models.CharField(
                    choices=[('new', 'Nowe'), ('replied', 'Odpowiedziano'), ('closed', 'Zamknięte')],
                    default='new',
                    max_length=30,
                )),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('room', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    to='core.room',
                )),
            ],
            options={
                'verbose_name': 'Zapytanie',
                'verbose_name_plural': 'Zapytania',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=100)),
                ('entity_name', models.CharField(max_length=100)),
                ('entity_id', models.BigIntegerField(null=True)),
                ('details', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={
                'verbose_name': 'Log audytu',
                'verbose_name_plural': 'Logi audytu',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='room',
            index=models.Index(fields=['slug'], name='room_slug_idx'),
        ),
        migrations.AddIndex(
            model_name='inquiry',
            index=models.Index(fields=['status'], name='inquiry_status_idx'),
        ),
        migrations.AddIndex(
            model_name='inquiry',
            index=models.Index(fields=['email'], name='inquiry_email_idx'),
        ),
    ]
