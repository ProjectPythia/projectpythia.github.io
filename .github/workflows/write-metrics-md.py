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

        # Markdown table
        headers = '| Project | Users |'
        separator = '| ' + ' | '.join(['-----'] * 2) + ' |'
        rows = []
        for key in user_data.keys():
            rows.append('| ' + key + ' | ' + user_data[key] + ' |')
        table = '\n'.join([headers, separator] + rows)
        f.write(table)
        f.write('\n\n')

        # Add plots
        f.write(f'![Users this Year]({this_year})\n\n')
        f.write(f'![Top Pages]({top_pages})\n\n')
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
