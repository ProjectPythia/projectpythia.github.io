---
kernelspec:
  name: python3
  display_name: Python 3
---

# Metrics

```{code-cell} python3
:tags: [remove-cell]

import datetime
import json
import os

import cartopy
import cartopy.io
import google
import matplotlib
import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np
import warnings

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest

# Project ID Numbers
PORTAL_ID = '266784902'
FOUNDATIONS_ID = '281776420'
COOKBOOKS_ID = '324070631'

# Access Secrets
PRIVATE_KEY_ID = os.environ.get('PRIVATE_KEY_ID')
# Ensure GH secrets doesn't introduce extra '\' new line characters (related to '\' being an escape character)
PRIVATE_KEY = os.environ.get('PRIVATE_KEY').replace('\\n', '\n')

credentials_dict = {
    'type': 'service_account',
    'project_id': 'cisl-vast-pythia',
    'private_key_id': PRIVATE_KEY_ID,
    'private_key': PRIVATE_KEY,
    'client_email': 'pythia-metrics-api@cisl-vast-pythia.iam.gserviceaccount.com',
    'client_id': '113402578114110723940',
    'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
    'token_uri': 'https://oauth2.googleapis.com/token',
    'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs',
    'client_x509_cert_url': 'https://www.googleapis.com/robot/v1/metadata/x509/pythia-metrics-api%40cisl-vast-pythia.iam.gserviceaccount.com',
    'universe_domain': 'googleapis.com',
}

try:
    client = BetaAnalyticsDataClient.from_service_account_info(credentials_dict)
except google.auth.exceptions.MalformedError as e:
    print('Malformed Error:', repr(e))
    # Insight into reason for failure without exposing secret key
    # 0: Secret not found, else malformed
    # 706: extra quote, 732: extra '\', 734: both
    print('Length of PRIVATE_KEY:', len(PRIVATE_KEY))

pre_project_date = '2020-03-31'
```


Last Updated: {eval}`str(datetime.datetime.now())`

This metrics page provides an overview of user activity collected by Google Analytics across the three pillars of Project Pythia: our portal which includes information about the project as well as our resource gallery, our Foundations book, and our Cookbooks gallery. Information is either all-time (from a pre-project start date of March 2020) or year-to-date as indicated and is updated nightly to provide real-time and automated insights into our engagement, impact, and audience reach. If you would like to request a different metrics analysis, timeframe, or view, please [open a GitHub issue](https://github.com/ProjectPythia/projectpythia.github.io/issues/new/choose).

## Table of Total Active Users by Project

```{code-cell} python3
:tags: [remove-cell]

def _format_rounding(value):
    """
    Helper function for rounding string displays. 1,232 -> 1.2K
    """
    return f'{round(value / 1000, 1):.1f}K'


# The rest of this file alternates between functions for requesting information from Google Analytics
# And functions that use that request image to form either a .json or a .png file to be used in write-metrics-md.py
def _run_total_users_report(property_id):
    """
    Function for requesting cumulative active users from a project since project start.
    """
    request = RunReportRequest(
        property=f'properties/{property_id}',
        dimensions=[],
        metrics=[Metric(name='activeUsers')],
        date_ranges=[DateRange(start_date=pre_project_date, end_date='today')],
    )
    response = client.run_report(request)

    total_users = 0
    for row in response.rows:
        total_users += int(row.metric_values[0].value)

    return _format_rounding(total_users)
```

This table displays the total active users of our 3 Pythia projects over the life of Project Pythia. Google analytics defines active users as the number of unique people who have visited the site and met certain [engagement requirements](https://support.google.com/analytics/answer/9234069?sjid=8697784525616937194-NC). You can read more from the [GA4 "Understand User Metrics" documentation](https://support.google.com/analytics/answer/12253918?hl=en).

```{code-cell} python3
:tags: [remove-cell]

portal_users = _run_total_users_report(PORTAL_ID)
foundations_users = _run_total_users_report(FOUNDATIONS_ID)
cookbooks_users = _run_total_users_report(COOKBOOKS_ID)
```

(table-total-users)=
| Project | All-Time Users |
| ----------- | ------------------------- |
| Portal | {eval}`portal_users` |
| Foundations | {eval}`foundations_users` |
| Cookbooks | {eval}`cookbooks_users` |

## Chart of Active Users by Project Since Year Start

```{code-cell} python3
:tags: [remove-cell]

def _run_active_users_this_year(property_id):
    """
    Function for requesting active users by day from a project since year start.
    """
    current_year = datetime.datetime.now().year
    start_date = f'{current_year}-01-01'

    request = RunReportRequest(
        property=f'properties/{property_id}',
        dimensions=[Dimension(name='date')],
        metrics=[Metric(name='activeUsers')],
        date_ranges=[DateRange(start_date=start_date, end_date='today')],
    )
    response = client.run_report(request)

    dates = []
    user_counts = []
    for row in response.rows:
        date_str = row.dimension_values[0].value
        date = datetime.datetime.strptime(date_str, '%Y%m%d')
        dates.append(date)
        user_counts.append(int(row.metric_values[0].value))

    # Days need to be sorted chronologically
    return zip(*sorted(zip(dates, user_counts), key=lambda x: x[0]))


def plot_projects_this_year(PORTAL_ID, FOUNDATIONS_ID, COOKBOOKS_ID):
    """
    Function for taking year-to-date active users by day and plotting it for each project.
    """
    portal_dates, portal_users = _run_active_users_this_year(PORTAL_ID)
    foundations_dates, foundations_users = _run_active_users_this_year(FOUNDATIONS_ID)
    cookbooks_dates, cookbooks_users = _run_active_users_this_year(COOKBOOKS_ID)

    # Plotting code
    plt.figure(figsize=(10, 5.5))
    plt.title('Year-to-Date Pythia Active Users', fontsize=15)

    plt.plot(portal_dates, portal_users, color='purple', label='Portal')
    plt.plot(foundations_dates, foundations_users, color='royalblue', label='Foundations')
    plt.plot(cookbooks_dates, cookbooks_users, color='indianred', label='Cookbooks')

    plt.legend(fontsize=12, loc='upper right')

    plt.xlabel('Date', fontsize=12)
    plt.show()

```

This line plot displays active users for our 3 Pythia projects (Portal in purple, Foundations in blue, and Cookbooks in salmon) since January 1st of the current year.

```{code-cell} python3
:tags: [remove-input]
:name: plot-active-users
:caption: Chart of active users by project since year start.

plot_projects_this_year(PORTAL_ID, FOUNDATIONS_ID, COOKBOOKS_ID)
```

## Chart of Top 5 Pages by Project

```{code-cell} python3
:tags: [remove-cell]

def _run_top_pages_report(property_id):
    """
    Function for requesting top 5 pages from a project.
    """
    request = RunReportRequest(
        property=f'properties/{property_id}',
        dimensions=[Dimension(name='pageTitle')],
        date_ranges=[DateRange(start_date=pre_project_date, end_date='today')],
        metrics=[Metric(name='screenPageViews')],
    )
    response = client.run_report(request)

    views_dict = {}
    for row in response.rows:
        page = row.dimension_values[0].value
        views = int(row.metric_values[0].value)
        views_dict[page] = views

    # Sort by views and grab the top 5
    top_pages = sorted(views_dict.items(), key=lambda item: item[1], reverse=True)[:5]
    # String manipulation on page titles "Cartopy - Pythia Foundations" -> "Cartopy"
    pages = [page.split('—')[0] for page, _ in top_pages]
    views = [views for _, views in top_pages]

    #  Reverse order of lists, so they'll plot with most visited page on top (i.e. last)
    return pages[::-1], views[::-1]
def plot_top_pages(PORTAL_ID, FOUNDATIONS_ID, COOKBOOKS_ID):
    """
    Function that takes the top 5 viewed pages for all 3 projects and plot them on a histogram.
    """
    portal_pages, portal_views = _run_top_pages_report(PORTAL_ID)
    foundations_pages, foundations_views = _run_top_pages_report(FOUNDATIONS_ID)
    cookbooks_pages, cookbooks_views = _run_top_pages_report(COOKBOOKS_ID)

    # Plotting code
    fig, ax = plt.subplots(figsize=(10, 5.5))
    plt.title('All-Time Top Pages', fontsize=15)

    y = np.arange(5)  # 0-4 for Cookbooks
    y2 = np.arange(6, 11)  # 6-10 for Foundations
    y3 = np.arange(12, 17)  # 12-16 for Portal

    bar1 = ax.barh(y3, portal_views, align='center', label='Portal', color='purple')
    bar2 = ax.barh(y2, foundations_views, align='center', label='Foundations', color='royalblue')
    bar3 = ax.barh(y, cookbooks_views, align='center', label='Cookbooks', color='indianred')

    y4 = np.append(y, y2)
    y4 = np.append(y4, y3)  # 0-4,6-19,12-6 for page labels to have a gap between projects
    pages = cookbooks_pages + foundations_pages + portal_pages  # List of all pages
    ax.set_yticks(y4, labels=pages, fontsize=12)

    # Adds round-formatted views label to end of each bar
    ax.bar_label(bar1, fmt=_format_rounding, padding=5, fontsize=10)
    ax.bar_label(bar2, fmt=_format_rounding, padding=5, fontsize=10)
    ax.bar_label(bar3, fmt=_format_rounding, padding=5, fontsize=10)

    ax.set_xscale('log')
    ax.set_xlim([10, 10**5])  # set_xlim must be after setting xscale to log
    ax.set_xlabel('Page Views', fontsize=12)

    plt.legend(fontsize=12, loc='lower right')
    plt.show()
```

This bar-chart displays the top 5 pages by project over the life of Project Pythia, as determined by screen page views. Screen page views refers to the number of times users viewed a page, including repeated visits. To learn more visit the [GA4 "API Dimensions & Metrics" page](https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema).

```{code-cell} python3
:tags: [remove-input]
:name: chart-top-five-pages
:caption: Bar chart of the top five pages by project over the life of Project Pythia

plot_top_pages(PORTAL_ID, FOUNDATIONS_ID, COOKBOOKS_ID)
```

## Map of Total Foundation Active Users by Country

```{code-cell} python3
:tags: [remove-cell]

# Disable cartopy warning
warnings.filterwarnings('ignore', category=cartopy.io.DownloadWarning)

def _run_usersXcountry_report(property_id):
    """
    Function for requesting users by country for a project.
    """
    request = RunReportRequest(
        property=f'properties/{property_id}',
        dimensions=[Dimension(name='country')],
        metrics=[Metric(name='activeUsers')],
        date_ranges=[DateRange(start_date=pre_project_date, end_date='today')],
    )
    response = client.run_report(request)

    user_by_country = {}
    for row in response.rows:
        country = row.dimension_values[0].value
        users = int(row.metric_values[0].value)
        user_by_country[country] = user_by_country.get(country, 0) + users

    return user_by_country
def plot_usersXcountry(FOUNDATIONS_ID):
    """
    Function for taking users by country for Pythia Foundations and plotting them on a map.
    """
    users_by_country = _run_usersXcountry_report(FOUNDATIONS_ID)

    # Google API Country names do not match Cartopy Country Shapefile names
    dict_api2cartopy = {
        'Tanzania': 'United Republic of Tanzania',
        'United States': 'United States of America',
        'Congo - Kinshasa': 'Democratic Republic of the Congo',
        'Bahamas': 'The Bahamas',
        'Timor-Leste': 'East Timor',
        'C\u00f4te d\u2019Ivoire': 'Ivory Coast',
        'Bosnia & Herzegovina': 'Bosnia and Herzegovina',
        'Serbia': 'Republic of Serbia',
        'Trinidad & Tobago': 'Trinidad and Tobago',
    }

    for key in dict_api2cartopy:
        users_by_country[dict_api2cartopy[key]] = users_by_country.pop(key)

    # Sort by views and grab the top 10 countries for a text box
    top_10_countries = sorted(users_by_country.items(), key=lambda item: item[1], reverse=True)[:10]
    top_10_text = '\n'.join(
        f'{country}: {_format_rounding(value)}' for i, (country, value) in enumerate(top_10_countries)
    )

    # Plotting code
    fig = plt.figure(figsize=(10, 4))
    ax = plt.axes(projection=cartopy.crs.PlateCarree(), frameon=False)
    ax.set_title('All-Time Pythia Foundations Users by Country', fontsize=15)

    shapefile = cartopy.io.shapereader.natural_earth(category='cultural', resolution='110m', name='admin_0_countries')
    reader = cartopy.io.shapereader.Reader(shapefile)
    countries = reader.records()

    colormap = plt.get_cmap('Blues')
    newcmp = colors.ListedColormap(colormap(np.linspace(0.2, 1, 128)))  # Truncate colormap to remove white hues
    newcmp.set_extremes(under='grey')

    norm = colors.LogNorm(vmin=1, vmax=max(users_by_country.values()))  # Plot on log scale
    mappable = cm.ScalarMappable(norm=norm, cmap=newcmp)

    # Loop through countries and plot their color
    for country in countries:
        country_name = country.attributes['SOVEREIGNT']
        if country_name in users_by_country.keys():
            facecolor = newcmp(norm(users_by_country[country_name]))
            ax.add_geometries(
                [country.geometry],
                cartopy.crs.PlateCarree(),
                facecolor=facecolor,
                edgecolor='white',
                linewidth=0.7,
                norm=matplotlib.colors.LogNorm(),
            )
        else:
            ax.add_geometries(
                [country.geometry], cartopy.crs.PlateCarree(), facecolor='grey', edgecolor='white', linewidth=0.7
            )

    # Add colorbar
    cax = fig.add_axes([0.05, -0.015, 0.7, 0.03])  # [x0, y0, width, height]
    cbar = fig.colorbar(mappable=mappable, cax=cax, spacing='uniform', orientation='horizontal', extend='min')
    cbar.set_label('Unique Users')

    # Add top 10 countries text
    props = dict(boxstyle='round', facecolor='white', edgecolor='white')
    ax.text(1.01, 0.5, top_10_text, transform=ax.transAxes, fontsize=12, verticalalignment='center', bbox=props)

    plt.show()
```

This map displays the number of active users per country for Pythia Foundations for the entire life of Project Pythia.

```{code-cell} python3
:tags: [remove-input]
:name: map-active-users-country
:caption: Map of the number of active users per country for Pythia Foundations for the entire life of Project Pythia.

plot_usersXcountry(FOUNDATIONS_ID)
```
