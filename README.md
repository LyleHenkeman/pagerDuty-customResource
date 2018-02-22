# Pager Duty Custom Resource

AWS Cloudformation Custom Resource to create ah p[agerDuty Service with an own integration directly out of cloudformation.

## Parameters

**servicesName**: Name of the pagerduty service created *mandatory*
**pagerDutyToken**: Your actual pagerduty token *mandatory*
**escalationPolicyId**: ID of the existing pagerduty escalation policy *mandatory*
**serviceUrgency**: Urgency of the service *default: high*
**description**: Description of your service

