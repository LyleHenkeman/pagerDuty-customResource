import requests
import json


def create_pager_duty(event):

    properties = event['ResourceProperties']

    # create headers for pagerduty call
    headers = compose_header(properties)
    #create service and return the service id
    service_id = create_service(properties, headers)
    #create integration for the given serviceId
    
    output = {
        'StackId': event['StackId'],
        'RequestId': event['RequestId'],
        'LogicalResourceId': event['LogicalResourceId'],
        'PhysicalResourceId': 'failed'
    }
    output['Status'] = 'FAILED'

    #create integration only if create service was successfull
    if (service_id):
        create_integration(service_id, headers)
        output['Status'] = 'SUCCESS'
        output['PhysicalResourceId'] = service_id 


    requests.put(event['ResponseURL'], data=json.dumps(output))


def compose_header(properties):
    headers = {
        'Accept': 'application/vnd.pagerduty+json;version=2',
        'Authorization': 'Token token={token}'.format(token=properties['PagerDutyToken']),
        'Content-type': 'application/json'
        }
    return headers

def create_service(properties, headers):
    service_url = 'https://api.pagerduty.com/services'

    service_payload = {
        'service': {
            'name': properties['ServicesName'],
            'description': properties['Description'],
            'escalation_policy': {
                'id': properties['EscalationPolicyId'],
                'type': 'escalation_policy'
            },
            'type': "service",
            'auto_resolve_timeout': 14400,
            'acknowledgement_timeout': 1800,
                    "incident_urgency_rule": {
                    "type": "constant",
                    "urgency": properties['ServiceUrgency']
                    }
        }
    }

    r = requests.post(service_url, data=json.dumps(service_payload), headers=headers)
    try:
        service_id = json.loads(r.text)['service']['id']
    except:
        return None

    return service_id

def create_integration(service_id ,headers):

    integration_url = 'https://api.pagerduty.com/services/{id}/integrations'.format(id=service_id)

    integration_payload = {
        'integration': {
            'type': 'generic_events_api_inbound_integration',
            'name': "Generic API Integration",
            "service": {
                "id": service_id,
                "type": "service"
            }
        }
    }

    r = requests.post(integration_url, data=json.dumps(integration_payload), headers=headers)
    integration_id = json.loads(r.text)['integration']['id']
