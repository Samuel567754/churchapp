from django.contrib import admin
from .models import (
    VolunteerOpportunity, VolunteerApplication, Testimonial, 
    FAQ, Survey, SurveyResponse, OutreachProgram ,Poll, PollOption, PollVote, Announcement, 
    CarouselItem
)
from django.utils.html import format_html


@admin.register(CarouselItem)
class CarouselItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_preview', 'description_preview', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    ordering = ['order']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 50px; width: auto;">', obj.image.url)
        elif obj.image_url:
            return format_html('<img src="{}" style="height: 50px; width: auto;">', obj.image_url)
        return "No Image"
    image_preview.short_description = 'Image Preview'

    def description_preview(self, obj):
        if obj.description:
            return obj.description[:50] + ('...' if len(obj.description) > 50 else '')
        return "No Description"
    description_preview.short_description = 'Description'

    def save_model(self, request, obj, form, change):
        obj.full_clean()  # Validate fields
        super().save_model(request, obj, form, change)

@admin.register(VolunteerOpportunity)
class VolunteerOpportunityAdmin(admin.ModelAdmin):
    list_display = ('title', 'ministry', 'is_active', 'start_date', 'end_date')
    search_fields = ('title', 'description')
    list_filter = ('ministry', 'is_active', 'start_date')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(VolunteerApplication)
class VolunteerApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'opportunity', 'application_date', 'accepted')
    list_filter = ('accepted', 'application_date')
    search_fields = ('user__username', 'opportunity__title')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('user', 'approved', 'date_submitted')
    list_filter = ('approved', 'date_submitted')
    search_fields = ('user__username', 'content')


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('question',)


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'description')


@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = ('survey', 'user', 'submitted_at')
    search_fields = ('survey__title', 'user__username')


@admin.register(OutreachProgram)
class OutreachProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('name', 'description')


# Registering the Poll model
@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('question', 'is_active', 'created_at')
    search_fields = ('question',)
    list_filter = ('is_active', 'created_at')

# Registering the PollOption model
@admin.register(PollOption)
class PollOptionAdmin(admin.ModelAdmin):
    list_display = ('poll', 'option_text')
    search_fields = ('option_text',)
    list_filter = ('poll',)

# Registering the PollVote model
@admin.register(PollVote)
class PollVoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'option', 'get_poll')
    search_fields = ('user__username', 'option__option_text', 'option__poll__question')
    list_filter = ('option__poll',)

    def get_poll(self, obj):
        return obj.option.poll
    get_poll.short_description = 'Poll'

    
@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'importance_level', 'date_posted', 'is_active')
    list_filter = ('status', 'importance_level', 'is_active')
    search_fields = ('title', 'content')