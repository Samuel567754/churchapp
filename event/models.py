from django.db import models
from django.contrib.auth.models import User
from membership.models import Ministry
from contact.models import Staff
from django.core.validators import MinValueValidator
from django.utils.text import slugify
from django.utils.timezone import now
from contact.models import SocialMediaMixin, ImageMixin


# EVENT MODEL
class Event(ImageMixin):
    EVENT_TYPES = [
        ('service', 'Church Service'),
        ('workshop', 'Workshop'),
        ('youth', 'Youth Event'),
        ('community', 'Community Event'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=200, blank=True)
    organizer = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)
    registration_required = models.BooleanField(default=False)
    max_attendees = models.PositiveIntegerField(
        null=True, blank=True, validators=[MinValueValidator(1)]
    )
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    attendees = models.ManyToManyField(User, through='EventRegistration', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    
# IMAGE GALLERY
class GalleryImage(ImageMixin):
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title if self.title else "Unnamed Image"



# EVENT REGISTRATION
class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['event', 'user']
        ordering = ['-registration_date']

    def __str__(self):
        return f"{self.user.username} registered for {self.event.title}"


class OutreachProgram(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=255)
    organizers = models.ManyToManyField(Staff, related_name='outreach_programs')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_date']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ChurchCalendar(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date', 'time']

    def __str__(self):
        return f"{self.title} on {self.date}"


