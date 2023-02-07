import re


PATTERN_NAME = re.compile(r"^\w.{0,}$")

TASK_STATUS = [
    ('important', 'important'),
    ('medium', 'medium'),
    ('small', 'small')
]

EX_STATUS = [
    ('completed', 'completed'),
    ('in_process', 'in_process')
]