from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Metric,
    RunReportRequest,
)

def run_total_users_report(property_id): 
    client = BetaAnalyticsDataClient()

    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[],
        metrics=[Metric(name="activeUsers")],
        date_ranges=[DateRange(start_date="2020-03-31", end_date="today")],
    )
    response = client.run_report(request)
  
    total_users = 0
    for row in response.rows:
        total_users += int(row.metric_values[0].value)
    return total_users
