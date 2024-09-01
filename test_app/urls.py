from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views
router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'flat', views.FlatCategoryViewSet, basename='flat_category')
router.register(r'materials', views.MaterialViewSet)

urlpatterns = [
    path('upload/', views.UploadExcelAPIView.as_view()),
    path('test/', views.TestAPIView.as_view()),
] + router.urls
