from django.contrib import admin
from .models import Donation, Asset


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('donor', 'amount', 'purpose', 'payment_method', 'date', 'is_recurring', 'transaction_id')
    list_filter = ('purpose', 'payment_method', 'is_recurring', 'date')
    search_fields = ('donor__username', 'transaction_id', 'notes')
    actions = ['mark_as_recurring', 'unmark_as_recurring']

    def mark_as_recurring(self, request, queryset):
        queryset.update(is_recurring=True)
        self.message_user(request, f"{queryset.count()} donations marked as recurring.")
    mark_as_recurring.short_description = "Mark selected donations as recurring"

    def unmark_as_recurring(self, request, queryset):
        queryset.update(is_recurring=False)
        self.message_user(request, f"{queryset.count()} donations unmarked as recurring.")
    unmark_as_recurring.short_description = "Unmark selected donations as recurring"


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('name', 'purchase_date', 'value', 'condition')
    list_filter = ('condition', 'purchase_date')
    search_fields = ('name', 'description')

    actions = ['mark_as_good', 'mark_as_needs_repair', 'mark_as_damaged']

    def mark_as_good(self, request, queryset):
        queryset.update(condition='Good')
        self.message_user(request, f"{queryset.count()} assets marked as Good.")
    mark_as_good.short_description = "Mark selected assets as Good"

    def mark_as_needs_repair(self, request, queryset):
        queryset.update(condition='Needs Repair')
        self.message_user(request, f"{queryset.count()} assets marked as Needs Repair.")
    mark_as_needs_repair.short_description = "Mark selected assets as Needs Repair"

    def mark_as_damaged(self, request, queryset):
        queryset.update(condition='Damaged')
        self.message_user(request, f"{queryset.count()} assets marked as Damaged.")
    mark_as_damaged.short_description = "Mark selected assets as Damaged"
