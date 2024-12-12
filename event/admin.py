from django.contrib import admin
from .models import Event, EventRegistration, OutreachProgram, ChurchCalendar, GalleryImage
from django.utils.html import format_html


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'event_type', 'organizer', 'registration_required', 'max_attendees', 'image_preview')
    list_filter = ('event_type', 'registration_required', 'date')
    search_fields = ('title', 'description', 'organizer__name')
    prepopulated_fields = {'slug': ('title',)}
    actions = ['mark_as_registration_required', 'unmark_as_registration_required']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px;" />', obj.image.url)
        return "No Image"

    image_preview.short_description = "Image Preview"

    def mark_as_registration_required(self, request, queryset):
        queryset.update(registration_required=True)
        self.message_user(request, f"{queryset.count()} events updated to require registration.")
    mark_as_registration_required.short_description = "Mark selected events as requiring registration"

    def unmark_as_registration_required(self, request, queryset):
        queryset.update(registration_required=False)
        self.message_user(request, f"{queryset.count()} events updated to not require registration.")
    unmark_as_registration_required.short_description = "Mark selected events as not requiring registration"


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at', 'is_featured', 'image_preview')
    list_filter = ('is_featured',)
    search_fields = ('title', 'description')
    actions = ['mark_as_featured', 'unmark_as_featured']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px;" />', obj.image.url)
        return "No Image"

    image_preview.short_description = "Image Preview"

    def mark_as_featured(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, f"{queryset.count()} images marked as featured.")
    mark_as_featured.short_description = "Mark selected images as featured"

    def unmark_as_featured(self, request, queryset):
        queryset.update(is_featured=False)
        self.message_user(request, f"{queryset.count()} images unmarked as featured.")
    unmark_as_featured.short_description = "Unmark selected images as featured"



@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'registration_date')
    search_fields = ('event__title', 'user__username')


@admin.register(OutreachProgram)
class OutreachProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description', 'location')
    prepopulated_fields = {'slug': ('name',)}
    actions = ['mark_as_active', 'mark_as_inactive']

    def mark_as_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f"{queryset.count()} outreach programs marked as active.")
    mark_as_active.short_description = "Mark selected programs as active"

    def mark_as_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f"{queryset.count()} outreach programs marked as inactive.")
    mark_as_inactive.short_description = "Mark selected programs as inactive"


@admin.register(ChurchCalendar)
class ChurchCalendarAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time')
    search_fields = ('title', 'description')
    list_filter = ('date',)


