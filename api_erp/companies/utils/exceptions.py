from rest_framework.exceptions import APIException

class NotFoundEmployee(APIException):
    status_code = 404
    default_detail = 'Employee not found!'
    default_code = 'employee_not_found'

class GroupNotFound(APIException):
    status_code = 404
    default_detail = 'Group not found!'
    default_code = 'group_not_found'

class RequiredFields(APIException):
    status_code = 400
    default_detail = 'Please follow the submit pattern!'
    default_code = 'required_fields_error'

class TaskStatusNotFound(APIException):
    status_code = 404
    default_detail = 'Task status not found!'
    default_code = 'task_status_not_found'

class TaskNotFound(APIException):
    status_code = 404
    default_detail = 'Task not found!'
    default_code = 'task_not_found'


