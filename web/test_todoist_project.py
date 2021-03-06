import pytest
import time
import logging
import allure

from api.test_todoist_project import api_create_new_project, api_delete_project, api_get_project_details, \
    api_get_project_id_by_project_name, api_remove_projects_by_project_name, api_remove_project_by_project_id

from pages.web.todoist_login import TodoistLogin
from pages.web.todoist_leftNav import TodoistLeftNav
from pages.web.todoist_project import TodoistProject


@pytest.mark.P1
@pytest.mark.Project
@pytest.mark.Web
@allure.epic('Web')
@allure.feature('Feature - Project')
@allure.story('Story - User project')
@allure.testcase('Test Case  - User project displayed accordingly')
def test_validate_project(browser, api, user):

    # project name used for each automated test must be unique to ensure each test is standalone
    project_name = 'test_create_project'
    token = api['api_token']
    project_url = api['api_project_url']
    email = user['email']
    password = user['password']

    api_remove_projects_by_project_name(token, project_url, project_name)

    project_id = api_create_new_project(token, project_url, project_name)
    assert project_id is not None, 'Project id should not be None'

    # project name used for each automated test must be unique to ensure each test is standalone

    # Body
    login = TodoistLogin(browser)
    login.load()
    login.email_login(email, password)

    left_nav = TodoistLeftNav(browser)
    left_nav.get_main_menu()
    left_nav.select_a_project_by_project_name(project_name)

    project_page = TodoistProject(browser)

    # Check if the expected project title being displayed
    project_page.check_project_title_is_displayed(project_name)