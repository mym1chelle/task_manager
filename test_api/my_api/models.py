from django.db import models
from django.core.validators import RegexValidator
from test_api.my_api.constants import PATTERN_NAME, TASK_STATUS, EX_STATUS


class Task(models.Model):
    name = models.CharField(
        max_length=200,
        null=False,
        validators=[
            RegexValidator(
                regex=PATTERN_NAME,
                message='first_symbol can`t be a special symbol'
            )
        ]
    )
    description = models.TextField()
    status = models.CharField(max_length=20, choices=TASK_STATUS)
    start_date = models.DateTimeField(auto_now_add=True)
    execution_status = models.CharField(
        max_length=20,
        default='in_process',
        choices=EX_STATUS
    )
