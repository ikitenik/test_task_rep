from django.urls import path

from . import views

urlpatterns = [
    path('materials/', views.MaterialAPIView.as_view()),
    path('materials/<int:pk>/', views.MaterialAPIView.as_view()),
    path('upload/', views.UploadExcelAPIView.as_view()),
]
