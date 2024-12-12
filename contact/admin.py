from django.contrib import admin
from .models import Staff, Contact, Notification, NewsletterSubscription, Newsletter

# Staff Admin
class StaffAdmin(admin.ModelAdmin):
    list_display = ('user', 'position', 'is_active', 'order', 'phone', 'email', 'image')
    list_filter = ('is_active',)
    search_fields = ('user__username', 'position', 'bio', 'facebook', 'twitter', 'instagram', 'linkedin', 'youtube')
    ordering = ['order']
    fieldsets = (
        (None, {
            'fields': ('user', 'position', 'bio', 'phone', 'email', 'order', 'is_active')
        }),
        ('Social Media Links', {
            'fields': ('facebook', 'twitter', 'instagram', 'linkedin', 'youtube')
        }),
        ('Image', {
            'fields': ('image',)
        }),
    )

admin.site.register(Staff, StaffAdmin)

# Contact Admin
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'email', 'date_sent')
    list_filter = ('date_sent',)
    search_fields = ('name', 'email', 'subject')

admin.site.register(Contact, ContactAdmin)


# Notification Admin
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('title', 'user__username')
    ordering = ['-created_at']

admin.site.register(Notification, NotificationAdmin)


# Newsletter Subscription Admin
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    list_filter = ('subscribed_at',)
    search_fields = ('email',)

admin.site.register(NewsletterSubscription, NewsletterSubscriptionAdmin)


# Newsletter Admin
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_sent', 'is_sent')
    list_filter = ('is_sent', 'date_sent')
    search_fields = ('title', 'content')
    ordering = ['-date_sent']

admin.site.register(Newsletter, NewsletterAdmin)
