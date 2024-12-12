from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Member, Membership, MemberDirectory

# Signal to create or update Member when Membership is created
@receiver(post_save, sender=Membership)
def create_or_update_member(sender, instance, created, **kwargs):
    """Ensure a Member instance is created or updated when a Membership is added."""
    if created:
        Member.objects.get_or_create(
            user=instance.user,
            defaults={
                'phone': '',
                'address': '',
                'baptized': False,
            }
        )


# Signal to create or update Membership when Member is created
@receiver(post_save, sender=Member)
def create_or_update_membership(sender, instance, created, **kwargs):
    """Ensure a Membership instance is created or updated when a Member is added."""
    if created:
        Membership.objects.get_or_create(
            user=instance.user,
            defaults={
                'join_date': instance.date_joined,
                'membership_type': 'Regular',  # Default membership type
            }
        )


# Automatically create or update MemberDirectory when Member is created
@receiver(post_save, sender=Member)
def create_or_update_member_directory(sender, instance, created, **kwargs):
    """Ensure a MemberDirectory instance is created when a Member is added."""
    if created:
        # Check if MemberDirectory already exists, update if needed
        member_directory, created = MemberDirectory.objects.get_or_create(
            user=instance.user,
            defaults={'phone_number': instance.phone or '', 'address': instance.address or ''}
        )

        # If it already exists, update the details
        if not created:
            member_directory.phone_number = instance.phone or ''
            member_directory.address = instance.address or ''
            member_directory.save()


# Update MemberDirectory when Membership is created
@receiver(post_save, sender=Membership)
def update_member_directory_from_membership(sender, instance, created, **kwargs):
    """Update the MemberDirectory when a Membership is created."""
    if created:
        member_directory, _ = MemberDirectory.objects.get_or_create(user=instance.user)
        if not member_directory.address:
            member_directory.address = "Updated from Membership"  # Example update
        member_directory.save()


# Delete Member when Membership is deleted
@receiver(post_delete, sender=Membership)
def delete_member_on_membership_delete(sender, instance, **kwargs):
    """Delete the associated Member when a Membership is deleted."""
    try:
        member = Member.objects.get(user=instance.user)
        member.delete()
    except Member.DoesNotExist:
        pass  # No Member to delete


# Delete Membership when Member is deleted
@receiver(post_delete, sender=Member)
def delete_membership_on_member_delete(sender, instance, **kwargs):
    """Delete the associated Membership when a Member is deleted."""
    try:
        membership = Membership.objects.get(user=instance.user)
        membership.delete()
    except Membership.DoesNotExist:
        pass  # No Membership to delete
