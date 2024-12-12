from django.contrib import admin
from .models import Ministry, Member, Membership, MemberDirectory, Attendance
from django.utils.html import format_html


@admin.register(Ministry)
class MinistryAdmin(admin.ModelAdmin):
    list_display = ('name', 'leader', 'meeting_time', 'location', 'is_active', 'social_media_links', 'image_preview')
    list_filter = ('is_active', 'age_group', 'created_at')
    search_fields = ('name', 'description', 'location')
    prepopulated_fields = {'slug': ('name',)}

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px;" />', obj.image.url)
        return "No Image"

    image_preview.short_description = "Image Preview"

    def social_media_links(self, obj):
        links = []
        if obj.facebook:
            links.append(f'<a href="{obj.facebook}" target="_blank">Facebook</a>')
        if obj.twitter:
            links.append(f'<a href="{obj.twitter}" target="_blank">Twitter</a>')
        if obj.instagram:
            links.append(f'<a href="{obj.instagram}" target="_blank">Instagram</a>')
        if obj.linkedin:
            links.append(f'<a href="{obj.linkedin}" target="_blank">LinkedIn</a>')
        if obj.youtube:
            links.append(f'<a href="{obj.youtube}" target="_blank">YouTube</a>')
        return format_html(" | ".join(links)) if links else "No Links"

    social_media_links.short_description = "Social Media Links"

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'ministry', 'date_joined', 'baptized')
    list_filter = ('baptized', 'ministry', 'date_joined')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'phone')


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'membership_type', 'join_date')
    list_filter = ('membership_type', 'join_date')
    search_fields = ('user__username', 'membership_type')


@admin.register(MemberDirectory)
class MemberDirectoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address')
    search_fields = ('user__username', 'address')


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'date', 'status')
    list_filter = ('status', 'date', 'event')
    search_fields = ('user__username', 'event__name')
    actions = ['mark_as_present', 'mark_as_absent']

    def mark_as_present(self, request, queryset):
        queryset.update(status='present')
        self.message_user(request, f"{queryset.count()} attendance records marked as present.")
    mark_as_present.short_description = "Mark selected as present"

    def mark_as_absent(self, request, queryset):
        queryset.update(status='absent')
        self.message_user(request, f"{queryset.count()} attendance records marked as absent.")
    mark_as_absent.short_description = "Mark selected as absent"
