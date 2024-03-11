import json
import os

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Metric, RunReportRequest

PORTAL_ID = os.environ['portal_id']
FOUNDATIONS_ID = os.environ['foundations_id']
COOKBOOKS_ID = os.environ['cookbook_id']


def _run_total_users_report(property_id):
    """Fetches total users for a given property ID

    Args:
        property_id: The Google Analytics 4 property ID

    Returns:
        int: The total number of active users
    """

    client = BetaAnalyticsDataClient()

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


def get_metrics(portal_id, foundations_id, cookbooks_id):
    """Retrieves total users for specified GA4 properties and writes to file if changes are significant."""

    metrics_dict = {}
    metrics_dict['portal_users'] = _run_total_users_report(str(portal_id))
    metrics_dict['foundations_users'] = _run_total_users_report(str(foundations_id))
    metrics_dict['cookbooks_users'] = _run_total_users_report(str(cookbooks_id))

    return metrics_dict  # Return the metrics dictionary


def write_metrics(metrics_dict):
    """Reads existing metrics, compares for significant change, and writes to file if necessary."""

    # Read existing user counts (handle potential file absence)
    try:
        with open('user_metrics.json') as f:
            user_data = json.load(f)
    except FileNotFoundError:
        user_data = {}

    # Define a threshold for significant change (adjust as needed)
    threshold = 100
    has_significant_change = False
    for property, user_count in metrics_dict.items():
        existing_count = user_data.get(property, 0)
        if abs(existing_count - user_count) > threshold:
            user_data[property] = user_count
            has_significant_change = True

    # Write to file if significant change detected
    if has_significant_change:
        with open('user_metrics.json', 'w') as outfile:
            json.dump(metrics_dict, outfile)
        return 1  # Signal significant change (optional)
    else:
        return 0  # Signal no significant change (optional)


if __name__ == '__main__':
    metrics = get_metrics(PORTAL_ID, FOUNDATIONS_ID, COOKBOOKS_ID)
    exit_code = write_metrics(metrics)
    if exit_code == 1:
        print('Significant change detected in user metrics.')
    else:
        print('No significant change in user metrics.')
