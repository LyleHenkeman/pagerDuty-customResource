import requests
import json

def delete_pager_duty(event):

    properties = event['ResourceProperties']
    #delete service for given ID
    delete_service(event['PhysicalResourceId'], properties)

    output = {'StackId': event['StackId'], 'RequestId': event['RequestId'],
              'LogicalResourceId': event['LogicalResourceId'], 'PhysicalResourceId': str(event['PhysicalResourceId']),
              'Status': 'SUCCESS'}

    requests.put(event['ResponseURL'], data=json.dumps(output))


def delete_service(id, properties):
    url = 'https://api.pagerduty.com/services/{id}'.format(id=id)
    headers = {
        'Accept': 'application/vnd.pagerduty+json;version=2',
        'Authorization': 'Token token={token}'.format(token=properties['PagerDutyToken'])
    }
    r = requests.delete(url, headers=headers)