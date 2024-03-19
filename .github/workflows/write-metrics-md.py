import datetime
import json


def process_user_data(json_file, top_pages, map, md_file):
    with open(json_file, 'r') as f:
        user_data = json.load(f)

    with open(md_file, 'w') as f:
        f.write('# Metrics \n\n')
        f.write(f'Last Updated: {datetime.datetime.now()}\n\n')

        headers = '| Project | Views |'
        separator = '| ' + ' | '.join(['-----'] * 2) + ' |'
        rows = []
        for key in user_data.keys():
            rows.append('| ' + key + ' | ' + user_data[key] + ' |')
        table = '\n'.join([headers, separator] + rows)
        f.write(table)
        f.write('\n\n')

        f.write(f'![Top Pages]({top_pages})')
        f.write(f'![Users by Country]({map})')
        f.write('\n')
    f.close()


if __name__ == '__main__':
    json_file = 'portal/metrics/user_metrics.json'
    top_pages = 'metrics/toppages.png'
    map = 'metrics/bycountry.png'
    md_file = 'portal/metrics.md'
    process_user_data(json_file, top_pages, map, md_file)
