from django.db.models.signals import post_save
from django.dispatch import receiver
from post.models import Like, Comment
from .models import Notification


@receiver(post_save, sender=Like)
def create_like_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.post.user, post=instance.post, notification_type="like")


@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created and not instance.is_reply:
        Notification.objects.create(user=instance.post.user, post=instance.post, notification_type="comment")


@receiver(post_save, sender=Comment)
def create_reply_notification(sender, instance, created, **kwargs):
    if created and instance.is_reply:
        Notification.objects.create(user=instance.parent.user, comment=instance.parent, notification_type="reply")
