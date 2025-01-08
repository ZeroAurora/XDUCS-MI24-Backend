from django.db.models.signals import post_save
from django.dispatch import receiver
from post.models import Like, Content
from .models import Notification


def notify_parents(content, notification_type, original_user):
    """Recursively notify all parents of a comment, excluding the original user"""
    if content.parent:
        if content.parent.user != original_user:
            Notification.objects.create(
                user=content.parent.user,
                content=content.parent,
                notification_type=notification_type
            )
        notify_parents(content.parent, notification_type, original_user)


@receiver(post_save, sender=Like)
def create_like_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.content.user,
            content=instance.content,
            notification_type="like"
        )


@receiver(post_save, sender=Content)
def create_comment_notification(sender, instance, created, **kwargs):
    if created and not instance.is_post:
        # Notify the parent content and all its ancestors
        notify_parents(instance, "comment", instance.user)
