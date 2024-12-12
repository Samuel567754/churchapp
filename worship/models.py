from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from contact.models import SocialMediaMixin, ImageMixin
from contact.models import Staff
from membership.models import Member


# SERVICE TYPE ENUM

class Sermon(ImageMixin):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    preacher = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True)
    date = models.DateField()
    scripture_reference = models.CharField(max_length=200, blank=True)
    video_url = models.URLField(blank=True, null=True)
    audio_file = models.FileField(upload_to='sermons/audio/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    series = models.ManyToManyField('SermonSeries', blank=True, related_name='sermons')
    tags = models.ManyToManyField('SermonTag', blank=True, related_name='sermons')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class SermonSeries(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='sermon_series/', blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class SermonTag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# SCHEDULE MODEL
class ServiceSchedule(models.Model):
    DAYS_OF_WEEK = [
        ('Sunday', 'Sunday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    ]

    day_of_week = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    time = models.TimeField()
    service_type = models.CharField(max_length=255)  # E.g., Worship, Bible Study
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.service_type} on {self.day_of_week} at {self.time}"


class Appointment(models.Model):
    class ServiceType(models.TextChoices):
        SUNDAY_SERVICE = 'Sunday', 'Sunday Service'
        TUESDAY_BIBLE_STUDY = 'Tuesday', 'Tuesday Bible Study'
        FRIDAY_PRAYER_MEETING = 'Friday', 'Friday Prayer Meeting'

    date = models.DateField()
    service_type = models.CharField(
        max_length=10,
        choices=ServiceType.choices,
        default=ServiceType.SUNDAY_SERVICE,
    )
    morning_devotion_leader = models.ForeignKey(
        'membership.Member', on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments_as_morning_leader'
    )
    song_leader = models.ForeignKey(
        'membership.Member', on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments_as_song_leader'
    )
    bible_study_leader_sunday = models.ForeignKey(
        'membership.Member', on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments_as_bible_study_leader_sunday'
    )
    preacher = models.ForeignKey(
        'membership.Member', on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments_as_sermon_leader'
    )
    first_prayer_leader = models.ForeignKey(
        'membership.Member', on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments_as_first_prayer_leader'
    )
    second_prayer_leader = models.ForeignKey(
        'membership.Member', on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments_as_second_prayer_leader'
    )
    third_prayer_leader = models.ForeignKey(
        'membership.Member', on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments_as_third_prayer_leader'
    )
    lord_supper_leader = models.ForeignKey(
        'membership.Member', on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments_as_lord_supper_leader'
    )
    lord_supper_helpers = models.ManyToManyField(
        'membership.Member', blank=True, related_name='appointments_as_lord_supper_helpers'
    )
    announcer = models.ForeignKey(
        'membership.Member', on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments_as_announcer'
    )
    bible_study_leader_tuesday = models.ForeignKey(
        'membership.Member', on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments_as_bible_study_leader_tuesday'
    )
    tuesday_service_leader = models.ForeignKey(
        'membership.Member', on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments_as_tuesday_service_leader'
    )
    friday_prayer_leader = models.ForeignKey(
        'membership.Member', on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments_as_friday_prayer_leader'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']
        constraints = [
            models.UniqueConstraint(fields=['date', 'service_type'], name='unique_appointment')
        ]

    def __str__(self):
        return f"{self.service_type} - {self.date}"




class Schedule(models.Model):
    RECURRING_CHOICES = [
        ('WEEKLY', 'Weekly'),
        ('MONTHLY', 'Monthly'),
        ('YEARLY', 'Yearly'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=200, blank=True)
    is_recurring = models.BooleanField(default=False)
    recurrence_pattern = models.CharField(
        max_length=100,
        choices=RECURRING_CHOICES,
        blank=True,
        help_text="E.g., 'Weekly', 'Monthly', 'Yearly'",
    )

    def __str__(self):
        return self.title


class LiveStream(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    stream_url = models.URLField()
    scheduled_time = models.DateTimeField()
    is_live = models.BooleanField(default=False)
    thumbnail = models.ImageField(upload_to='livestreams/')
    viewers_count = models.IntegerField(default=0)
    recorded_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title


class Resource(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='resources/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    
class PrayerRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request = models.TextField()
    date_requested = models.DateTimeField(auto_now_add=True)
    is_answered = models.BooleanField(default=False)

    def __str__(self):
        return f"Prayer Request by {self.user}"
