import json
import os
import base64
import hashlib

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Metric, RunReportRequest

PORTAL_ID = os.environ.get('PORTAL_ID')
FOUNDATIONS_ID = os.environ.get('FOUNDATIONS_ID')
COOKBOOKS_ID = os.environ.get('COOKBOOKS_ID')

#PRIVATE_KEY_ID = os.environ.get('PRIVATE_KEY_ID')
#PRIVATE_KEY = os.environ.get('PRIVATE_KEY').replace('$','\n')
#credentials_dict = {
#  "type": "service_account",
#  "project_id": "cisl-vast-pythia",
#  "private_key_id": PRIVATE_KEY_ID,
#  "private_key": PRIVATE_KEY,
#  "client_email": "pythia-metrics-api@cisl-vast-pythia.iam.gserviceaccount.com",
#  "client_id": "113402578114110723940",
#  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#  "token_uri": "https://oauth2.googleapis.com/token",
#  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/pythia-metrics-api%40cisl-vast-pythia.iam.gserviceaccount.com",
#  "universe_domain": "googleapis.com"
#}

ENCODED_CREDENTIALS = os.environ.get('ENCODED_CREDENTIALS')
if ENCODED_CREDENTIALS is None:
    print("OH NO")
    raise Exception("Encoded credentials secret not found!")
else:
    decoded_credentials = base64.b64decode(ENCODED_CREDENTIALS).decode('utf-8')
    credentials_dict = json.loads(decoded_credentials)
    
    client = BetaAnalyticsDataClient.from_service_account_info(credentials_dict)


def _run_total_users_report(property_id):
    request = RunReportRequest(
        property=f'properties/{property_id}',
        dimensions=[],
        metrics=[Metric(name='activeUsers')],
        date_ranges=[DateRange(start_date='2020-03-31', end_date='today')],
    )

    response = client.run_report(request)

    total_users = 0
    for row in response.rows:
        total_users += int(row.metric_values[0].value)

    return total_users


def get_metrics():
    metrics_dict = {}
    metrics_dict['Portal'] = _run_total_users_report(str(PORTAL_ID))
    metrics_dict['Foundations'] = _run_total_users_report(str(FOUNDATIONS_ID))
    metrics_dict['Cookbooks'] = _run_total_users_report(str(COOKBOOKS_ID))

    with open('user_metrics.json', 'w') as outfile:
        json.dump(metrics_dict, outfile)


if __name__ == '__main__':
    get_metrics()
