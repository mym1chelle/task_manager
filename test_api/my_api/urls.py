from django.urls import path
from .views import TaskAPIView, UpdateTaskAPIView, CloseTaskAPIView

urlpatterns = [
    path('tasks/', TaskAPIView.as_view()),
    path('tasks/<int:pk>/', UpdateTaskAPIView.as_view()),
    path('tasks/<int:pk>/close/', CloseTaskAPIView.as_view())
]
