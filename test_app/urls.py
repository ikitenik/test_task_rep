from django.urls import path

from . import views

urlpatterns = [
    path('categories/', views.CategoriesAPIView.as_view()),
    path('materials/', views.MaterialAPIView.as_view()),
    path('materials/<int:pk>/', views.MaterialAPIView.as_view()),
    path('material_types/', views.MaterialTypesAPIView.as_view()),
    path('material_types/<int:pk>/', views.MaterialTypesAPIView.as_view()),
    path('upload/', views.UploadExcelAPIView.as_view()),
]
