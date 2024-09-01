from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views
router = DefaultRouter()
router.register(r'categories/tree', views.TreeCategoryViewSet)
router.register(r'categories/list', views.ListCategoryViewSet, basename='list_category')
router.register(r'materials', views.MaterialViewSet)

urlpatterns = [
    path('upload/', views.UploadExcelAPIView.as_view()),
] + router.urls
