from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import date, timedelta
from .models import *
from rest_framework.serializers import ModelSerializer
from .serializers import MemberSerializer, AttendanceSerializer, EventSerializer
from django.db.models import Q
# Create your views here.

def hello(request):
    return HttpResponse("Hello World")


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit objects.
    """
    def has_permission(self, request, view):
        return(
            request.method in permissions.SAFE_METHODS or
            (request.user.is_authenticated and hasattr(request.user, 'membermodel') and
             request.user.membermodel.user_role == 'Admin'  
             )
        )

class MemberViewSet(viewsets.ModelViewSet):
    queryset = MemberModel.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    def get_queryset(self):
        user = self.request.user
        
        if not user.is_authenticated:
            return MemberModel.objects.none()
        if user.is_superuser:
            return MemberModel.objects.all()
        if not user.is_superuser:
            return MemberModel.objects.filter(user=user)
        member = getattr(user, 'membermodel', None)
        if member:
            return MemberModel.objects.all()
        return MemberModel.objects.filter(user=user)
        # return MemberModel.objects.filter(user=user)

    
class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = AttendanceModel.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    @action(detail=False, methods=['get'], url_path='heatmap/(?P<member_id>[^/.]+)')
    def heatmap(self, request, member_id=None):
        # Get attendance records for this member
        records = AttendanceModel.objects.filter(member_id=member_id).values("date", "is_present")
        attendance_map = {rec["date"]: rec["is_present"] for rec in records}

        # Generate last 365 days
        today = date.today()
        start_date = today - timedelta(days=364)
        data = {}
        sorted_dates = []

        current_date = start_date
        while current_date <= today:
            is_present = attendance_map.get(current_date, False)
            data[current_date.strftime("%Y-%m-%d")] = is_present
            sorted_dates.append(current_date.strftime("%Y-%m-%d"))
            current_date += timedelta(days=1)

        # Calculate streaks
        longest_streak = 0
        current_streak = 0
        temp_streak = 0

        for day in sorted_dates:
            if data[day]:
                temp_streak += 1
                longest_streak = max(longest_streak, temp_streak)
                if day == today.strftime("%Y-%m-%d"):
                    current_streak = temp_streak
            else:
                temp_streak = 0

        return Response({
            "heatmap": data,  # every day for the past year
            "current_streak": current_streak,
            "longest_streak": longest_streak
        })

class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    # def get_queryset(self):
    #     user = self.request.user

    #     if not user.is_authenticated:
    #         return EventModel.objects.none()

    #     member = getattr(user, 'membermodel', None)

    #     if user.is_superuser or (member and member.user_role == 'Admin'):
    #         return EventModel.objects.all()

    #     if member:
    #         return EventModel.objects.filter(members_participated=member).distinct()

    #     return EventModel.objects.none()

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return EventModel.objects.none()

        member = getattr(user, 'membermodel', None)

        # if user.is_superuser or (member and member.user_role == 'Admin'):
        if user.is_superuser:
            return EventModel.objects.all()
        if user and not user.is_superuser:
            return EventModel.objects.filter(user=user).distinct()

        if member:
            return EventModel.objects.filter(members_participated=member).distinct()

        return EventModel.objects.none()


    
    
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]



    

