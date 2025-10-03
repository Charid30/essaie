from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import SkillViewSet, UserSkillViewSet

router = DefaultRouter()
router.register('', SkillViewSet)
router.register('user-skills', UserSkillViewSet, basename='user-skill')

urlpatterns = [
    path('', include(router.urls)),
]
