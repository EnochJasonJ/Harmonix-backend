from django.urls import path, include
from .views import hello, MemberViewSet, AttendanceViewSet, EventViewSet, UserViewSet
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
    path('hello/', hello, name='hello'),
    path('', include(router.urls)),
]
