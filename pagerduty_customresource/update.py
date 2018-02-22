import requests
import json

def update_pager_duty(event):
    properties = event['ResourceProperties']
    update_service(event['PhysicalResourceId'])

    output = {'StackId': event['StackId'], 'RequestId': event['RequestId'],
              'LogicalResourceId': event['LogicalResourceId'], 'PhysicalResourceId': event['PhysicalResourceId'],
              'Status': 'SUCCESS'}

    requests.put(event['ResponseURL'], data=json.dumps(output))


def update_service(id):
    url = 'https://api.pagerduty.com/services/{id}'.format(id=id)
    headers = {
        'Accept': 'application/vnd.pagerduty+json;version=2',
        'Authorization': 'Token token={token}'.format(token=properties['PagerDutyToken']),
        'Content-type': 'application/json'
    }
    service_payload = {
        'service': {
            'name': properties['ServicesName'],
            'description': properties['ServiceDescription'],
            'escalation_policy': {
                'id': properties['EscalationPolicyId'],
                'type': 'escalation_policy'
            },
            'type': service,
            'auto_resolve_timeout': 14400,
            'acknowledgement_timeout': 1800,
                    "incident_urgency_rule": {
                    "type": "constant",
                    "urgency": properties['ServiceUrgency']
                    }
        }
    }

    r = requests.put(url, headers=headers, data=json.dumps(payload))