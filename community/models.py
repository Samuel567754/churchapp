from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from membership.models import Ministry, MemberDirectory
from contact.models import Staff
from django.core.exceptions import ValidationError

# VOLUNTEER OPPORTUNITIES
class VolunteerOpportunity(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    slug = models.SlugField(unique=True)  # Add the slug field here
    end_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=200, blank=True)
    ministry = models.ForeignKey(Ministry, on_delete=models.SET_NULL, null=True, blank=True, related_name="volunteer_opportunities")
    created_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_opportunities")
    is_active = models.BooleanField(default=True)
    volunteers = models.ManyToManyField(User, through='VolunteerApplication', related_name="volunteer_opportunities")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('volunteer_opportunity_detail', args=[self.id])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # Auto-generate slug based on title
        super().save(*args, **kwargs)


class VolunteerApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="volunteer_applications")
    opportunity = models.ForeignKey(VolunteerOpportunity, on_delete=models.CASCADE, related_name="applications")
    application_date = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ['user', 'opportunity']

    def __str__(self):
        return f"{self.user} - {self.opportunity}"


# TESTIMONIALS
class Testimonial(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="testimonials")
    content = models.TextField()
    date_submitted = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Testimonial by {self.user.get_full_name() if self.user else 'Anonymous'}"


# FAQ
class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.question


# SURVEYS AND RESPONSES
class Survey(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('survey_detail', args=[self.id])


class SurveyResponse(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="responses")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="survey_responses")
    response = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response to {self.survey.title} by {self.user}"


# OUTREACH PROGRAMS
class OutreachProgram(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=255)
    organizers = models.ManyToManyField(MemberDirectory, related_name="outreach_programs")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('outreach_program_detail', args=[self.id])
    
    
# POLL MODEL
class Poll(models.Model):
    question = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.question


# POLL OPTION MODEL
class PollOption(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.option_text} (Poll: {self.poll})"


# POLL VOTE
class PollVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    option = models.ForeignKey(PollOption, on_delete=models.CASCADE)
    poll = models.ForeignKey('Poll', on_delete=models.CASCADE)  # Make sure this field exists in the model

    def __str__(self):
        return f"{self.user} voted for {self.option}"
    
    
class Announcement(models.Model):
    # Choices for announcement status
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    # Choices for importance level
    IMPORTANCE_CHOICES = [
        ('urgent', 'Urgent'),
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]

    title = models.CharField(max_length=255)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft',  # Default status is 'draft'
    )
    importance_level = models.CharField(
        max_length=10,
        choices=IMPORTANCE_CHOICES,
        default='medium',  # Default importance level is 'medium'
    )

    def __str__(self):
        return self.title
    
    

class CarouselItem(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='carousel_images/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)  # Optional link for the carousel item
    is_active = models.BooleanField(default=True)  # To control visibility
    order = models.PositiveIntegerField(default=0)  # To control order of items

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title or f"Carousel Item {self.id}"

    def clean(self):
        # Ensure at least one of image or image_url is provided
        if not self.image and not self.image_url:
            raise ValidationError("Either 'image' or 'image_url' must be provided.")

