from django.urls import path, include
from .views import hello, MemberViewSet, AttendanceViewSet, EventViewSet, UserViewSet,request_password_reset, confirm_password_reset
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register('members', MemberViewSet, basename='member')
router.register('attendance', AttendanceViewSet, basename='attendance')
router.register('events', EventViewSet, basename='event')
router.register('users', UserViewSet, basename='user')


urlpatterns = [
    path('token/',TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/',TokenRefreshView.as_view(), name='token_refresh'),
    path('password-reset-request/', request_password_reset, name='password_reset_request'),
    path('password-reset-confirm/', confirm_password_reset, name='password_reset_confirm'),
    path('hello/', hello, name='hello'),
    path('', include(router.urls)),
]
