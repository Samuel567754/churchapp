from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.validators import MinValueValidator

# Abstract Model for Social Media Links
class SocialMediaMixin(models.Model):
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)

    class Meta:
        abstract = True


# Abstract Model for Image Fields
class ImageMixin(models.Model):
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)

    class Meta:
        abstract = True


# STAFF MODEL
class Staff(SocialMediaMixin, ImageMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name_plural = "Staff Members"
        indexes = [models.Index(fields=['position', 'is_active'])]

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.position}"


# Contact Model
class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['email', 'date_sent'])]
    
    def __str__(self):
        return self.subject


# NOTIFICATIONS Model
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Notification for {self.user.username} - {self.title}"


# Newsletter Subscription Model
class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['email'])]

    def __str__(self):
        return self.email


# NEWSLETTER Model
class Newsletter(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)
    recipients = models.ManyToManyField(User, blank=True)
    attachment = models.FileField(upload_to='newsletters/', blank=True, null=True)
    is_sent = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_sent']
    
    def __str__(self):
        return self.title
