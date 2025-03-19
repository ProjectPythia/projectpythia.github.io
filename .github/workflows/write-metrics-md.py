import json


def process_user_data(json_file, top_pages, this_year, map, md_file):
    """
    Function for writing portal/metrics.md from saved files output by get-metrics.py
    """
    with open(json_file, 'r') as f:
        user_data = json.load(f)

    with open(md_file, 'w') as f:
        f.write('# Metrics \n\n')
        now = user_data['Now']
        f.write(f'Last Updated: {now}')
        user_data.pop('Now')
        f.write('\n\n')

        # Intro description
        f.write(
            'This metrics page provides an overview of user activity collected by Google Analytics across the three pillars of Project Pythia: our portal which includes information about the project as well as our resource gallery, our Foundations book, and our Cookbooks gallery. Information is either all-time (from a pre-project start date of March 2020) or year-to-date as indicated and is updated nightly to provide real-time and automated insights into our engagement, impact, and audience reach. If you would like to request a different metrics analysis, timeframe, or view, please [open a GitHub issue](https://github.com/ProjectPythia/projectpythia.github.io/issues/new/choose).\n\n'
        )

        # Markdown table
        f.write('## Table of Total Active Users by Project\n\n')
        f.write(
            'This table displays the total active users of our 3 Pythia projects over the life of Project Pythia. Google analytics defines active users as the number of unique people who have visited the site and met certain [engagement requirements](https://support.google.com/analytics/answer/9234069?sjid=8697784525616937194-NC). You can read more from the [GA4 "Understand User Metrics" documentation](https://support.google.com/analytics/answer/12253918?hl=en).\n\n'
        )
        headers = '| Project | All-Time Users |'
        separator = '| ' + ' | '.join(['-----'] * 2) + ' |'
        rows = []
        for key in user_data.keys():
            rows.append('| ' + key + ' | ' + user_data[key] + ' |')
        table = '\n'.join([headers, separator] + rows)
        f.write(table)
        f.write('\n\n')

        # Add plots
        f.write('## Chart of Active Users by Project Since Year Start\n\n')
        f.write(
            'This line plot displays active users for our 3 Pythia projects (Portal in purple, Foundations in blue, and Cookbooks in salmon) since January 1st of the current year. Typically Foundations is our most visited project, but with all 3 displaying a cycle representative of the Monday-Friday work week.\n\n'
        )
        f.write(f'![Users this Year]({this_year})\n\n')

        f.write('## Chart of Top 5 Pages by Project\n\n')
        f.write(
            'This bar-chart displays the top 5 pages by project over the life of Project Pythia, as determined by screen page views. Screen page views refers to the number of times users viewed a page, including repeated visits. To learn more visit the [GA4 "API Dimensions & Metrics" page](https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema).\n\n'
        )
        f.write(f'![Top Pages]({top_pages})\n\n')

        f.write('## Map of Total Foundation Active Users by Country\n\n')
        f.write(
            'This map displays the number of active users per country for Pythia Foundations for the entire life of Project Pythia.\n\n'
        )
        f.write(f'![Users by Country]({map})\n\n')

    f.close()


if __name__ == '__main__':
    json_file = 'portal/metrics/user_metrics.json'  # Accessed from root repository

    # HTML is built from within `portal/` directory, so paths differ from json file.
    top_pages = 'metrics/toppages.png'
    this_year = 'metrics/thisyear.png'
    map = 'metrics/bycountry.png'

    md_file = 'portal/metrics.md'  # Written from root repository
    process_user_data(json_file, top_pages, this_year, map, md_file)
