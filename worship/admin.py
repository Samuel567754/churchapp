from django.contrib import admin
from .models import (
    Sermon, SermonSeries, SermonTag, ServiceSchedule, 
    Appointment, Schedule, LiveStream, Resource, PrayerRequest
)
from django.utils.html import format_html

# Inline Models
class SermonTagInline(admin.TabularInline):
    model = Sermon.tags.through
    extra = 1

class SermonSeriesInline(admin.TabularInline):
    model = Sermon.series.through
    extra = 1

class LordSupperHelpersInline(admin.TabularInline):
    model = Appointment.lord_supper_helpers.through
    extra = 1

# Sermon Admin
@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    list_display = ('title', 'preacher', 'date', 'is_featured', 'image_preview', 'video_link')
    list_filter = ('date', 'is_featured', 'series')
    search_fields = ('title', 'preacher__name', 'scripture_reference')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [SermonTagInline, SermonSeriesInline]

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px;" />', obj.image.url)
        return "No Image"

    image_preview.short_description = "Image Preview"

    def video_link(self, obj):
        if obj.video_url:
            return format_html('<a href="{}" target="_blank">Watch Video</a>', obj.video_url)
        return "No Video"

    video_link.short_description = "Video Link"

# Sermon Series Admin
@admin.register(SermonSeries)
class SermonSeriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)

# Sermon Tag Admin
@admin.register(SermonTag)
class SermonTagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

# Service Schedule Admin
@admin.register(ServiceSchedule)
class ServiceScheduleAdmin(admin.ModelAdmin):
    list_display = ('service_type', 'day_of_week', 'time')
    list_filter = ('day_of_week',)
    search_fields = ('service_type', 'description')

# Appointment Admin
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('date', 'service_type', 'preacher', 'song_leader')
    list_filter = ('service_type', 'date')
    search_fields = ('preacher__name', 'song_leader__name')
    inlines = [LordSupperHelpersInline]

# Schedule Admin
@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time', 'is_recurring')
    list_filter = ('is_recurring', 'recurrence_pattern')
    search_fields = ('title', 'description')

# Live Stream Admin
@admin.register(LiveStream)
class LiveStreamAdmin(admin.ModelAdmin):
    list_display = ('title', 'scheduled_time', 'is_live', 'viewers_count')
    list_filter = ('is_live', 'scheduled_time')
    search_fields = ('title', 'description')

# Resource Admin
@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')
    search_fields = ('title', 'description')
    
    
# PrayerRequest Admin
@admin.register(PrayerRequest)
class PrayerRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'request', 'date_requested', 'is_answered')
    list_filter = ('is_answered', 'date_requested')
    search_fields = ('user__username', 'request')
