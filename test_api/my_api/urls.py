from django.urls import path
from test_api.my_api.views import TaskAPIView, UpdateDeleteTaskAPIView, CloseTaskAPIView

urlpatterns = [
    path('tasks/', TaskAPIView.as_view()),
    path('tasks/<int:pk>/', UpdateDeleteTaskAPIView.as_view()),
    path('tasks/<int:pk>/close/', CloseTaskAPIView.as_view())
]
