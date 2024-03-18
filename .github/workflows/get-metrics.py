import json
import math
import os

import cartopy
import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest

PORTAL_ID = os.environ['PORTAL_ID']
FOUNDATIONS_ID = os.environ['FOUNDATIONS_ID']
COOKBOOKS_ID = os.environ['COOKBOOKS_ID']

PRIVATE_KEY_ID = os.environ.get('PRIVATE_KEY_ID')
PRIVATE_KEY = os.environ.get('PRIVATE_KEY')
print(len(PRIVATE_KEY))

credentials_dict = {
    'type': 'service_account',
    'project_id': 'cisl-vast-pythia',
    'private_key_id': str(PRIVATE_KEY_ID),
    'private_key': str(PRIVATE_KEY),
    'client_email': 'pythia-metrics-api@cisl-vast-pythia.iam.gserviceaccount.com',
    'client_id': '113402578114110723940',
    'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
    'token_uri': 'https://oauth2.googleapis.com/token',
    'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs',
    'client_x509_cert_url': 'https://www.googleapis.com/robot/v1/metadata/x509/pythia-metrics-api%40cisl-vast-pythia.iam.gserviceaccount.com',
    'universe_domain': 'googleapis.com',
}

print(credentials_dict)
client = BetaAnalyticsDataClient.from_service_account_info(credentials_dict)


def _format_rounding(value):
    return f'{round(value / 1000, 1):.1f}K'


def run_total_users_report(property_id):
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

    return _format_rounding(total_users)


def _run_top_pages_report(property_id):
    request = RunReportRequest(
        property=f'properties/{property_id}',
        dimensions=[Dimension(name='pageTitle')],
        date_ranges=[DateRange(start_date='2020-03-31', end_date='today')],
        metrics=[Metric(name='screenPageViews')],
    )

    response = client.run_report(request)

    page_views = {}
    for row in response.rows:
        page = row.dimension_values[0].value
        views = int(row.metric_values[0].value)
        page_views[page] = views

    top_10_pages = sorted(page_views.items(), key=lambda item: item[1], reverse=True)[:10]
    top_10_pages_dict = {page: views for page, views in top_10_pages}

    return top_10_pages_dict


def plot_top_pages(foundations_id, cookbooks_id):
    foundations_page_views = _run_top_pages_report(foundations_id)
    foundations_pages = []
    foundations_sorted = {k: v for k, v in sorted(foundations_page_views.items(), key=lambda item: item[1])}
    foundations_views = foundations_sorted.values()
    for key in foundations_sorted:
        newkey = key.split('—')[0]
        foundations_pages.append(newkey)

    cookbooks_page_views = _run_top_pages_report(cookbooks_id)
    cookbooks_pages = []
    cookbooks_sorted = {k: v for k, v in sorted(cookbooks_page_views.items(), key=lambda item: item[1])}
    cookbooks_views = cookbooks_sorted.values()
    for key in cookbooks_page_views:
        newkey = key.split('—')[0]
        cookbooks_pages.insert(0, newkey)

    pages = cookbooks_pages + foundations_pages

    fig, ax = plt.subplots()
    plt.title('Most Popular Pages')

    views_max = int(math.ceil(max(foundations_views) / 10000.0)) * 10000
    ax.set_xlim([0, views_max])

    y = np.arange(10)
    y2 = np.arange(11, 21)
    y3 = np.append(y, y2)

    bar1 = ax.barh(y2, foundations_views, align='center', label='Foundations', color='royalblue')
    bar2 = ax.barh(y, cookbooks_views, align='center', label='Cookbooks', color='indianred')

    ax.set_yticks(y3, labels=pages)

    ax.bar_label(bar1, fmt=_format_rounding)
    ax.bar_label(bar2, fmt=_format_rounding)

    plt.legend()
    plt.savefig('bypage.png', bbox_inches='tight')


def _run_usersXcountry_report(foundations_id):
    request = RunReportRequest(
        property=f'properties/{foundations_id}',
        dimensions=[Dimension(name='country')],
        metrics=[Metric(name='activeUsers')],
        date_ranges=[DateRange(start_date='2020-03-31', end_date='today')],
    )

    response = client.run_report(request)

    user_by_country = {}
    for row in response.rows:
        country = row.dimension_values[0].value
        users = int(row.metric_values[0].value)
        user_by_country[country] = user_by_country.get(country, 0) + users

    return user_by_country


def plot_usersXcountry(foundations_id):
    users_by_country = _run_usersXcountry_report(foundations_id)

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

    top_10_countries = sorted(users_by_country.items(), key=lambda item: item[1], reverse=True)[:10]
    top_10_text = '\n'.join(
        f'{country}: {_format_rounding(value)}' for i, (country, value) in enumerate(top_10_countries)
    )

    fig = plt.figure(figsize=(10, 4))
    ax = plt.axes(projection=cartopy.crs.PlateCarree(), frameon=False)
    ax.set_title('Pythia Foundations Unique Users by Country')

    shapefile = cartopy.io.shapereader.natural_earth(category='cultural', resolution='110m', name='admin_0_countries')
    reader = cartopy.io.shapereader.Reader(shapefile)
    countries = reader.records()

    colormap = plt.get_cmap('Blues')
    colormap.set_extremes(under='grey')
    vmax = int(math.ceil(max(users_by_country.values()) / 100.0)) * 100
    norm = colors.LogNorm(vmin=1, vmax=vmax)
    mappable = cm.ScalarMappable(norm=norm, cmap=colormap)

    for country in countries:
        country_name = country.attributes['SOVEREIGNT']
        if country_name in users_by_country.keys():
            facecolor = colormap((users_by_country[country_name] / 105))

            ax.add_geometries(
                [country.geometry], cartopy.crs.PlateCarree(), facecolor=facecolor, edgecolor='white', linewidth=0.7
            )
        else:
            ax.add_geometries(
                [country.geometry], cartopy.crs.PlateCarree(), facecolor='grey', edgecolor='white', linewidth=0.7
            )

    cax = fig.add_axes([0.1, -0.015, 0.67, 0.03])
    fig.colorbar(mappable=mappable, cax=cax, spacing='uniform', orientation='horizontal', extend='min')

    props = dict(boxstyle='round', facecolor='white', edgecolor='white')
    ax.text(1.01, 0.5, top_10_text, transform=ax.transAxes, fontsize=9, verticalalignment='center', bbox=props)

    plt.tight_layout()
    plt.savefig('bycountry.png', bbox_inches='tight')


def get_metrics():
    metrics_dict = {}
    metrics_dict['Portal'] = run_total_users_report(str(PORTAL_ID))
    metrics_dict['Foundations'] = run_total_users_report(str(FOUNDATIONS_ID))
    metrics_dict['Cookbooks'] = run_total_users_report(str(COOKBOOKS_ID))
    with open('user_metrics.json', 'w') as outfile:
        json.dump(metrics_dict, outfile)

    plot_top_pages(str(FOUNDATIONS_ID), str(COOKBOOKS_ID))

    plot_usersXcountry(str(FOUNDATIONS_ID))


if __name__ == '__main__':
    get_metrics()
