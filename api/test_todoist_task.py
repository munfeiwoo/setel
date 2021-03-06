import json
import requests
import time
import uuid
import pytest
import allure

from api.test_todoist_project import api_create_new_project, api_delete_project, api_get_project_details, \
    api_remove_project_by_project_id


def api_get_project_tasks(token, project_task_url, project_id):
    response = requests.get(
        project_task_url,
        params={
            "project_id": project_id
        },
        headers={
            "Authorization": "Bearer {}".format(token)
        })
    assert response.status_code == 200, 'Response status should be 200'
    return response.json()


def api_create_project_task(token, project_task_url, project_id, content, due):
    response = requests.post(
        project_task_url,
        data=json.dumps({
            "content": content,
            "due_string": due,
            "project_id": project_id
        }),
        headers={
            "Content-Type": "application/json",
            "X-Request-Id": str(uuid.uuid4()),
            "Authorization": "Bearer {}".format(token)
        })
    assert response.status_code == 200, 'Response status should be 200'
    task = response.json()
    assert task['content'] == content, 'Task content should be "{}"'.format(content)
    return task['id']


def api_get_project_task_by_name(token, project_task_url, project_id, task_name):
    tasks = api_get_project_tasks(token, project_task_url, project_id)
    for task in tasks:
        if task['content'] == task_name:
            return task['content']


def api_get_project_task_id_by_name(token, project_task_url, project_id, task_name):
    tasks = api_get_project_tasks(token, project_task_url, project_id)
    for task in tasks:
        if task['content'] == task_name:
            return task['id']


def api_reopen_task(token, project_task_url, task_id):
    reopen_url = project_task_url + "/{}".format(task_id) + "/reopen"
    response = requests.post(reopen_url,
                             headers={"Authorization": "Bearer {}".format(token)})
    assert response.status_code == 204, 'Response status should be 204'


def api_close_task(token, project_task_url, task_id):
    close_url = project_task_url + "/{}".format(task_id) + "/close"
    response = requests.post(close_url,
                             headers={"Authorization": "Bearer {}".format(token)})
    assert response.status_code == 204, 'Response status should be 204'


@pytest.mark.P1
@pytest.mark.Task
@pytest.mark.API
@allure.epic('API')
@allure.feature('Feature - Task')
@allure.story('Story - Task')
@allure.testcase('Test Case  - create and get tasks details using API')
def test_create_and_get_tasks_details(api_test_config):
    project_name = 'project_task1'
    task_title = 'testing 12345'
    task_due = '26 June 2020'
    token = api_test_config['api_token']
    project_task_url = api_test_config['api_project_task_url']
    project_url = api_test_config['api_project_url']

    project_id = api_create_new_project(token, project_url, project_name)
    assert project_id is not None, 'Project id should not be None'

    task_id = api_create_project_task(token, project_task_url, project_id, task_title, task_due)
    assert task_id is not None, 'Task id should not be None'
    assert api_get_project_task_by_name(token, project_task_url, project_id, task_title) == task_title, \
        'Task title should be "{}"'.format(task_title)

    api_close_task(token, project_task_url, task_id)
    api_reopen_task(token, project_task_url, task_id)
    assert api_get_project_task_by_name(token, project_task_url, project_id, task_title) == task_title, \
        'Task title should be "{}"'.format(task_title)

    time.sleep(2)

    api_remove_project_by_project_id(token, project_url, project_id)
