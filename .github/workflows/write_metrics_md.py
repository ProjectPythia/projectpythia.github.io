import json


def process_user_data(user_data_file, markdown_file):
    """
    Reads user data from a JSON file and writes it to a markdown file.

    Args:
        user_data_file: Path to the JSON file containing user data.
        markdown_file: Path to the output markdown file.
    """

    with open(user_data_file, 'r') as f:
        user_data = json.load(f)

    table_header = '| Portal | Foundations | Cookbooks |\n'
    table_row = f"| {' | '.join([str(user_data[key]) for key in user_data])} |\n"
    table = table_header + table_row
    # Write processed data to markdown file
    with open(markdown_file, 'w') as f:
        f.write('# Metrics \n\n')
        f.write('Total Users:\n')
        f.write(table)


if __name__ == '__main__':
    user_data_file = 'user_data.json'
    markdown_file = '../portal/metrics.md'
    process_user_data(user_data_file, markdown_file)
    print('User data report generated: ', markdown_file)
