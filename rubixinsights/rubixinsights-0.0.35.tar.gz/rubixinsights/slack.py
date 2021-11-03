import requests
import json

def write_message_to_slack(slack_webhook_url: str, message: str):
    payload = {'text': message}
    headers = {'Content-type': 'application/json'}
    requests.post(slack_webhook_url, data=json.dumps(payload), headers=headers)





def report_failure_to_slack_wrapper(slack_webhook_url: str):
    """Callback to send slack message if pipeline fails

    :param slack_webhook_url: slack webhook url
    :type slack_webhook_url: str
    """
    def report_failure_to_slack(context):
        channel = context['dag'].tags[0]
        execution_date = context['execution_date']
        execution_date = f"{execution_date.year}-{execution_date.month}-{execution_date.day}"
        message = f"[Pipeline Error] [{channel}] [{execution_date}]"
        payload = {'text': message}
        headers = {'Content-type': 'application/json'}
        requests.post(slack_webhook_url, data=json.dumps(payload), headers=headers)
    return report_failure_to_slack
