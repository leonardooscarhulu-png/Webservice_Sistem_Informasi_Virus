from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import KategoriViewSet, VirusViewSet

router = DefaultRouter()
router.register(r'kategori', KategoriViewSet, basename='kategori')
router.register(r'virus', VirusViewSet, basename='virus')

urlpatterns = [
    path('', include(router.urls)),
]