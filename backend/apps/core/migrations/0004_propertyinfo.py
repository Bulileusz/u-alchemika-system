from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_inquiry_index_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='PropertyInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('booking_url', models.URLField(blank=True)),
                ('facebook_url', models.URLField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('check_in', models.CharField(blank=True, max_length=100)),
                ('check_out', models.CharField(blank=True, max_length=100)),
                ('pets_policy', models.TextField(blank=True)),
                ('parking_info', models.TextField(blank=True)),
                ('payment_info', models.TextField(blank=True)),
                ('breakfast_info', models.TextField(blank=True)),
                ('cancellation_policy', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'Dane obiektu',
                'verbose_name_plural': 'Dane obiektu',
            },
        ),
    ]
