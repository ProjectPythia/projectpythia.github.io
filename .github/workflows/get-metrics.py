import json

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Metric, RunReportRequest


def _run_total_users_report(property_id):
    """Fetches total users for a given property ID

    Args:
        property_id: The Google Analytics 4 property ID

    Returns:
        int: The total number of active users
    """

    client = BetaAnalyticsDataClient()

    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[],
        metrics=[Metric(name='activeUsers')],
        date_ranges=[DateRange(start_date='2020-03-31', end_date='today')],
    )

    response = client.run_report(request)

    total_users = 0
    for row in response.rows:
        total_users += int(row.metric_values[0].value)

    return total_users


def _get_metrics():
    """Retrieves total users for all GA4 properties and stores them in a dictionary

    Returns:
        dict: A dictionary containing property names as keys and user counts as values
    """

    metrics_dict = {}
    metrics_dict['portal_users'] = _run_total_users_report({{secrets.GA4_PORTAL_ID}})
    metrics_dict['foundations_users'] = _run_total_users_report({{secrets.GA4_FOUNDATIONS_ID}})
    metrics_dict['cookbooks_users'] = _run_total_users_report({{secrets.GA4_COOKBOOKS_ID}})
    return metrics_dict


def write_metrics():
    """Retrieves metrics, checks for significant change, and writes to file."""

    metrics_dict = _get_metrics()

    # Read existing user counts
    try:
        with open('user_metrics.json') as f:
            user_data = json.load(f)
    except FileNotFoundError:
        user_data = {}  # Handle case where file doesn't exist

    # Check for significant difference (configurable threshold)
    threshold = 100
    has_significant_change = FALSE
    for property, user_count in metrics_dict.items():
        if abs(user_data.get(property, 0) - user_count) > threshold:
            user_data[property] = user_count
            has_significant_change = TRUE
    if has_significant_change:
        with open('user_metrics.json', 'w') as outfile:
            json.dump(metrics_dict, outfile)
        return 1
    else:
        return 0


write_metrics()
