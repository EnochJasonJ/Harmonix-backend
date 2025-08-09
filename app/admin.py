from django.contrib import admin
from .models import MemberModel, AttendanceModel, EventModel
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django import forms
import secrets

@admin.register(MemberModel)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'club', 'role', 'position', 'present_days_count')
    class Media:
        js = ('admin/js/club_role_filter.js',)

@admin.register(EventModel)
class EventAdmin(admin.ModelAdmin):
    filter_horizontal = ('members_participated',)  # Better UI

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "members_participated":
            # Example: only show members from Harmonix
            kwargs["queryset"] = MemberModel.objects.all()
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def get_changeform_initial_data(self, request):
        # Ensures no members are preselected by default
        initial = super().get_changeform_initial_data(request)
        initial['members_participated'] = []  # empty selection
        return initial


# admin.site.register(EventModel)
admin.site.register(AttendanceModel)


class CustomUserAdmin(UserAdmin):
    # Add email to the add form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    def save_model(self, request, obj, form, change):
        is_new_user = not change
        old_email = None

        if not is_new_user and obj.pk:
            old_email = User.objects.filter(pk=obj.pk).values_list('email', flat=True).first()

        # ✅ Save user first (retains password entered via admin)
        super().save_model(request, obj, form, change)

        # 🟡 Skip sending email if no email or not relevant case
        if is_new_user and obj.email:
            print(f"🟡 New user '{obj.username}' created with email. Sending now.")
        elif not old_email and obj.email:
            print(f"🟢 Email just added for existing user '{obj.username}'. Sending now.")
        else:
            return

        # ✅ Use the password they entered in the admin form
        password = form.cleaned_data.get("password1")
        if not password:
            print(f"❌ No password found to send.")
            return

        # ✅ Send email with the correct password
        send_mail(
            subject="Your Harmonix Club Credentials",
            message=f"""Hi {obj.username},

    Your account has been created successfully for Harmonix Club 🎵.

    🔐 Login Credentials:
    Username: {obj.username}
    Password: {password}

    Please login and change your password immediately for security.

    - Harmonix Club Admin""",
            from_email='enochjason06@gmail.com',
            recipient_list=[obj.email],
            fail_silently=False
        )
        print(f"✅ Email sent to {obj.email}")



admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
