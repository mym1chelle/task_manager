from django.test import TestCase
from django.urls import reverse
from test_api.my_api.models import Task
import json


class UserTestCase(TestCase):
    fixtures = ['tasks.json']

    def setUp(self):
        self.task1 = Task.objects.get(pk=1)
        self.task2 = Task.objects.get(pk=2)
        self.task3 = Task.objects.get(pk=3)
        self.task4 = Task.objects.get(pk=4)

    def test_tasks_list(self):
        """Test tasks list"""
        response = self.client.get(reverse('tasks'))
        tasks_json = response.json()
        task1, task2, task3, task4 = tasks_json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(task1['name'], 'task_one')
        self.assertEqual(task1['description'], 'description_one')
        self.assertEqual(task1['status'], 'small')
        self.assertEqual(task1['execution_status'], 'in_process')
        self.assertEqual(task2['name'], 'task_two')
        self.assertEqual(task2['description'], 'description_two')
        self.assertEqual(task2['status'], 'medium')
        self.assertEqual(task2['execution_status'], 'in_process')
        self.assertEqual(task3['name'], 'task_three')
        self.assertEqual(task3['description'], 'description_three')
        self.assertEqual(task3['status'], 'important')
        self.assertEqual(task3['execution_status'], 'completed')
        self.assertEqual(task4['name'], 'task_four')
        self.assertEqual(task4['description'], 'description_four')
        self.assertEqual(task4['status'], 'small')
        self.assertEqual(task4['execution_status'], 'in_process')

    def test_create_task(self):
        """Test create task"""
        new_task = {
            'name': 'task_five',
            'description': 'description_five',
            'status': 'small'
        }
        response = self.client.post(
            path=reverse('tasks'),
            data=new_task
        )

        self.assertEqual(response.status_code, 201)

        new_task = Task.objects.get(name=new_task['name'])
        self.assertEqual('task_five', new_task.name)
        self.assertEqual('description_five', new_task.description)
        self.assertTrue('small', new_task.status)
        self.assertTrue('in_process', new_task.execution_status)

    def test_create_task_with_special_symbol(self):
        """Test create task with special symbol"""
        new_task = {
            'name': '#task_five',
            'description': 'description_five',
            'status': 'small'
        }
        response = self.client.post(
            path=reverse('tasks'),
            data=new_task
        )
        self.assertEqual(response.status_code, 400)
        error = response.json()
        self.assertEqual(
            'first symbol can`t be a special symbol',
            error['name'][0]
        )

    def test_change_task(self):
        """Test change task"""

        task2 = self.task2

        changed_task = {
            'name': 'changed_name',
            'description': 'changed_description',
            'status': 'small',
        }
        response = self.client.put(
            reverse('update_delete',
                    args=(task2.id,)
                    ),
            data=json.dumps(changed_task),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

        new_task = Task.objects.get(name=changed_task['name'])
        self.assertEqual('changed_name', new_task.name)
        self.assertEqual('changed_description', new_task.description)
        self.assertEqual('small', new_task.status)

    def test_close_task(self):
        """Test close task"""

        task1 = self.task1

        changed_task = {
            "execution_status": "completed"
        }
        response = self.client.put(
            reverse('task_close',
                    args=(task1.id,)
                    ),
            data=json.dumps(changed_task),
            content_type='application/json')

        self.assertEqual(response.status_code, 200)
        closed_task = Task.objects.get(id=task1.id)
        self.assertEqual('completed', closed_task.execution_status)

    def test_close_not_exists_task(self):
        """Test close not exists task"""

        changed_task = {
            "execution_status": "completed"
        }
        response = self.client.put(
            reverse('task_close',
                    args=(12,)
                    ),
            data=json.dumps(changed_task),
            content_type='application/json')

        error = response.json()
        self.assertEqual(response.status_code, 500)
        self.assertEqual(error['detail'], 'object does not exists')


    def test_filter_by_names(self):
        """Filter the tasks by status"""
        filtered_by_name = f'{reverse("tasks")}?task_name=task_t'
        response = self.client.get(filtered_by_name)
        self.assertEqual(response.status_code, 200)
        first_task, second_task = response.json()
        self.assertTrue('task_t' in first_task['name'])
        self.assertTrue('task_t' in second_task['name'])

    def test_filter_by_date(self):
        """Filter the tasks by date"""
        filtered_by_min_date = f'{reverse("tasks")}?min_date=2021-02-07'
        response = self.client.get(filtered_by_min_date)
        self.assertEqual(response.status_code, 200)
        first_task, second_task, third_task, fourth_task\
            = response.json()
        self.assertTrue(first_task['start_date'] > '2021-02-07')
        self.assertTrue(second_task['start_date'] > '2021-02-07')
        self.assertTrue(third_task['start_date'] > '2021-02-07')
        self.assertTrue(fourth_task['start_date'] > '2021-02-07')

    def test_filter_by_status(self):
        """Filter by status"""
        filtered_by_status = f'{reverse("tasks")}?status=small'
        response = self.client.get(filtered_by_status)
        self.assertEqual(response.status_code, 200)
        first_task, second_task = response.json()
        self.assertEqual('small', first_task['status'])
        self.assertEqual('small', second_task['status'])

    def test_filter_by_execution_status(self):
        """Filter the tasks by execution status"""
        filtered_by_status = f'{reverse("tasks")}?ex=completed'
        response = self.client.get(filtered_by_status)
        self.assertEqual(response.status_code, 200)
        first_task = response.json()[0]
        self.assertEqual('completed', first_task['execution_status'])

    def test_delete_task(self):
        """Test delete task"""
        task = self.task4
        response = self.client.delete(
            reverse('update_delete', args=(task.id,)),
        )
        self.assertEqual(response.status_code, 204)
        self.assertRaises(Task.DoesNotExist)
