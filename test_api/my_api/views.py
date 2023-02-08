from rest_framework import generics
from rest_framework.views import APIView
import django_filters.rest_framework
from rest_framework.response import Response
from test_api.my_api.serializers import (
    CreateUpdateTaskSerializer,
    ShowTaskSerializer,
    UpdateTaskStatusSerializer,
)
from test_api.my_api.models import Task
from test_api.my_api.filters import TaskFilter


class TaskAPIView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = TaskFilter
    serializer_class = CreateUpdateTaskSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ShowTaskSerializer(queryset, many=True)
        return Response(serializer.data)


class CloseTaskAPIView(APIView):

    def get(self, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            task = Task.objects.get(id=pk)
        except Task.DoesNotExist:
            return Response({'detail': 'Object does not exists'}, status=422)
        serializer = ShowTaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            instance = Task.objects.get(id=pk)
        except Task.DoesNotExist:
            return Response({'errors': 'Object does not exists'})

        serializer = UpdateTaskStatusSerializer(
            data=request.data,
            instance=instance
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        result = ShowTaskSerializer(instance)
        return Response(result.data)


class UpdateDeleteTaskAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CreateUpdateTaskSerializer
    queryset = Task.objects.all()
