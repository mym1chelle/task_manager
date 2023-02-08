from rest_framework import serializers
from test_api.my_api.models import Task


class CreateUpdateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'name',
            'description',
            'status',
        ]


class ShowTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id',
            'name',
            'description',
            'status',
            'start_date',
            'execution_status'
        ]


class UpdateTaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'execution_status'
        ]
