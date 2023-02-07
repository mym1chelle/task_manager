from django_filters import rest_framework as f
from test_api.my_api.models import Task
from test_api.my_api.constants import TASK_STATUS, EX_STATUS


class TaskFilter(f.FilterSet):
    task_name = f.CharFilter(field_name='name', lookup_expr='icontains')
    min_date = f.DateFilter(field_name='start_date', lookup_expr='gte')
    max_date = f.DateFilter(field_name='start_date', lookup_expr='lte')
    ex = f.ChoiceFilter(field_name='execution_status', choices=EX_STATUS)
    status = f.ChoiceFilter(field_name='status', choices=TASK_STATUS)

    class Meta:
        model = Task
        fields = ['task_name', 'min_date', 'max_date', 'status', 'ex']
