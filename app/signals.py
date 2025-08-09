from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver
from .models import AttendanceModel, MemberModel , EventModel
from django.contrib.auth.models import User
from django.core.mail import send_mail
import secrets

@receiver(post_save, sender=AttendanceModel)
@receiver(post_delete, sender=AttendanceModel)
def update_present_days_signal(sender, instance, **kwargs):
    if instance.member:
        instance.member.update_present_days()
        

@receiver(m2m_changed, sender=EventModel.members_participated.through)
def update_event_counts_signal(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        if action == "post_clear":
            members = MemberModel.objects.all()
        else:
            members = MemberModel.objects.filter(pk__in=pk_set)

        for member in members:
            member.event_counts = member.events_participated.count()
            member.save()

# @receiver(post_save, sender=User)
# def send_credentials_to_users(sender, instance, created, **kwargs):
#     if created:
#         if not instance.email:
#             print("❌ No email provided. Skipping email sending.")
#             return
#         password = secrets.token_urlsafe(8)
#         instance.set_password(password)
#         print("Signal fired: User created.")
#         print("Attempting to send email to:", instance.email)
#         print("Generated password:", password)

#         # Save password without triggering signal again
#         User.objects.filter(pk=instance.pk).update(password=instance.password)

#         send_mail(
#             subject="Your Harmonix Club Credentials",
#             message=f"""Hi {instance.username},

# Your account has been created successfully for Harmonix Club 🎵.

# 🔐 Login Credentials:
# Username: {instance.username}
# Password: {password}

# Please login and change your password immediately for security.

# - Harmonix Club Admin""",
#             from_email='enochjason06@gmail.com',
#             recipient_list=[instance.email],
#             fail_silently=False
#         )