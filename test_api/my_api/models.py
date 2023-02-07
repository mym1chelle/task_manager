from django.db import models
from rest_framework.exceptions import APIException
from .constants import PATTERN_NAME, TASK_STATUS, EX_STATUS


def validate_first_char(string: str):
    first_symbol = string[0]
    if not PATTERN_NAME.match(first_symbol):
        raise APIException(
            detail=f'{first_symbol} is a special symbol'
        )


class Task(models.Model):
    name = models.CharField(max_length=200, null=False, validators=[validate_first_char])
    description = models.TextField()
    status = models.CharField(max_length=20, choices=TASK_STATUS)
    start_date = models.DateTimeField(auto_now_add=True)
    execution_status = models.CharField(max_length=20, default='in_process', choices=EX_STATUS)
