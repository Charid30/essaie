from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRegistrationView, CustomAuthToken, UserContactViewSet,LogoutView, ProfileViewSet, UserAdminViewSet ,  PasswordResetRequestView, PasswordResetConfirmView, ChangePasswordView

router = DefaultRouter()
router.register('profiles', ProfileViewSet, basename='profile')
router.register('admin-users', UserAdminViewSet, basename='admin-user')
router.register('contacts', UserContactViewSet, basename='contacts')
urlpatterns = [
    path('signup/', UserRegistrationView.as_view(), name='signup'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-reset-request/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]

urlpatterns += router.urls
