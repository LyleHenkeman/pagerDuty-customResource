from __future__ import print_function

from pagerduty_customresource.create import create_pager_duty
from pagerduty_customresource.delete import delete_pager_duty
from pagerduty_customresource.update import update_pager_duty


def handler(event, context):
    request_type = event['RequestType']

    if request_type == 'Create':
        return create_pager_duty(event)
    elif request_type == 'Delete':
        return delete_pager_duty(event)
    elif request_type == 'Update':
        return update_pager_duty(event)
    else:
        raise 'Unknown request type {}'.format(request_type)
