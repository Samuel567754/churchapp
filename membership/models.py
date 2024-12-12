from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from contact.models import Staff, SocialMediaMixin, ImageMixin
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


# MINISTRY MODEL
class Ministry(SocialMediaMixin, ImageMixin):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    leader = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)
    meeting_time = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    meeting_schedule = models.TextField(help_text="Detailed meeting schedule")
    age_group = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Ministries"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


# MEMBER MODEL
class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    date_joined = models.DateField(auto_now_add=True)
    baptized = models.BooleanField(default=False)
    ministry = models.ForeignKey(Ministry, on_delete=models.SET_NULL, null=True, blank=True, related_name="members")
    photo = models.ImageField(upload_to='members/', blank=True, null=True)

    class Meta:
        ordering = ['user__username']

    def __str__(self):
        return self.user.get_full_name() or self.user.username


# MEMBERSHIP MODEL
class Membership(models.Model):
    MEMBERSHIP_TYPES = [
        ('Regular', 'Regular'),
        ('Elder', 'Elder'),
        ('Youth', 'Youth'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    join_date = models.DateField()
    membership_type = models.CharField(max_length=255, choices=MEMBERSHIP_TYPES)

    class Meta:
        verbose_name_plural = "Memberships"

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.membership_type}"


# MEMBER DIRECTORY MODEL
class MemberDirectory(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    photo = models.ImageField(upload_to='members/', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Member Directories"

    def __str__(self):
        return f"{self.user.username}'s Directory"


# ATTENDANCE MODEL
class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey('event.Event', on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)

    class Meta:
        verbose_name_plural = "Attendance Records"
        unique_together = ('user', 'date', 'event')

    def __str__(self):
        name = self.user.get_full_name() or self.user.username
        return f"{name} - {self.date} - {self.status}"




# SIGNALS TO SYNC MEMBER AND MEMBERSHIP MODELS
# @receiver(post_save, sender=Membership)
# def create_or_update_member(sender, instance, created, **kwargs):
#     if created:
#         # Create a Member if it doesn't exist
#         Member.objects.get_or_create(
#             user=instance.user,
#             defaults={
#                 'phone': '',
#                 'address': '',
#                 'baptized': False,
#             }
#         )


# @receiver(post_save, sender=Member)
# def create_or_update_membership(sender, instance, created, **kwargs):
#     if created:
#         # Create a Membership if it doesn't exist
#         Membership.objects.get_or_create(
#             user=instance.user,
#             defaults={
#                 'join_date': instance.date_joined,
#                 'membership_type': 'Regular',  # Default membership type
#             }
#         )


# @receiver(post_delete, sender=Membership)
# def delete_member_on_membership_delete(sender, instance, **kwargs):
#     try:
#         member = Member.objects.get(user=instance.user)
#         member.delete()
#     except Member.DoesNotExist:
#         pass


# @receiver(post_delete, sender=Member)
# def delete_membership_on_member_delete(sender, instance, **kwargs):
#     try:
#         membership = Membership.objects.get(user=instance.user)
#         membership.delete()
#     except Membership.DoesNotExist:
#         pass