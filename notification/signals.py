from django.db.models.signals import post_save
from django.dispatch import receiver
from post.models import Like, Content
from .models import Notification

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
        if instance.parent.user != instance.user:
            Notification.objects.create(
                user=instance.parent.user,
                content=instance.parent,
                notification_type="comment"
            )
