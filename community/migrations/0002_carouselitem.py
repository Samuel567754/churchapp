# Generated by Django 5.1.3 on 2024-11-21 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarouselItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='carousel_images/')),
                ('image_url', models.URLField(blank=True, null=True)),
                ('link', models.URLField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]