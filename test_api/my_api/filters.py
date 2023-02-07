from django_filters import rest_framework as f
from .models import Task


class MyFilter(f.FilterSet):
    task_name = f.CharFilter(field_name='name', lookup_expr='icontains')
    min_date = f.DateFilter(field_name='start_date', lookup_expr='gte')
    max_date = f.DateFilter(field_name='start_date', lookup_expr='lte')
    status = f.CharFilter(field_name='status', lookup_expr='iexact')
    ex = f.CharFilter(field_name='execution_status', lookup_expr='iexact')

    class Meta:
        model = Task
        fields = ['task_name', 'min_date', 'max_date', 'status', 'ex']