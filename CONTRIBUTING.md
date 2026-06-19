# Development and infrastructure guide

This document contains information specific to contributing to the
Project Pythia Portal. Please first refer to [Guide for Contributing to Project Pythia](https://projectpythia.org/contributing) for overall
contribution guidelines (such as detailed description of Project
Pythia structure, forking, repository cloning, branching, etc.).

## Add a blog post
Within the `portal/posts/[YEAR]` folder add your `.md` blog file with the following heading:

```
---

date: YYYY-MM-DD
author: github-handle
tags: [sample-tag]
---
```

To display the post, you need to add the file path in the `myst.yml` configuration file under `toc:` -> `- title: Blog` -> `children:`. Please add the newest blog post at the top of the blog file list. This is temporary until we have better blog infrastructure.

## Build the documentation / portal website

The portal site is built with [MyST-MD](https://mystmd.org/).

When testing new content it helps to build and view the site. GitHub Actions automatically builds a preview when you open a pull request and posts the link in the PR. You can also build it locally, as described below.

### Building the site

The simplest build uses [`nox`](https://nox.thea.codes/), which creates its own environment with MyST. You don't need conda or the `pythia` environment to build or preview the site. This builds every page except the metrics page (see [Building the metrics page](#building-the-metrics-page) below for that).

Install nox once (for example `pip install nox`), then run from the repository root:

```bash
nox -s docs-live   # serve with live reload at localhost:3000
nox -s docs        # build the static HTML once
```

A link to [localhost:3000](http://localhost:3000) should appear in your terminal when serving. More information on setting up a [local test server is available here](https://developer.mozilla.org/en-US/docs/Learn/Common_questions/set_up_a_local_testing_server).

#### Install `pre-commit` hooks

This repository includes `pre-commit` hooks (defined in
`.pre-commit-config.yaml`). The `pre-commit` package comes with the `pythia` conda environment described below, or you can `pip install pre-commit`. Install the hooks once with:

```bash
pre-commit install
```

#### Building the metrics page

The metrics page runs live queries against the Google Analytics API, so it needs more than the simple build:

- The `pythia` conda environment, which has the required packages.
- Google Analytics credentials (see [Setting up Credentials](#setting-up-credentials) below).
- MyST run with `--execute`, so the page's code actually runs.

From the `portal` directory, use [conda](https://docs.conda.io/) to set up the environment:

```bash
cd projectpythia.github.io/portal
conda env update -f ../environment.yml
```

This creates the `pythia` environment, or adds any new packages if you already have it. Then activate it and build with execution turned on:

```bash
conda activate pythia
myst build --html --execute
```

It's a good idea to keep the environment's packages up to date with `conda update --all` while it's active.

## Instructions for interacting with the Google Analytics API

### Setting up the Virtual Environment

Analytics must be run on a virtual environment. To create and activate this environment, with the necessary `google-analytics-data` package, the terminal commands are:

```
python -m venv analytics-api-env
source analytics-api-env/bin/activate
pip install google-analytics-data
```

Replace 'analytics-api-env' with any new environment name. Also, `pip install` any other packages you may want for your analytics work.

### Setting up Credentials

To interact with the Google Analytics API locally you need to download the credentials file. This file has been uploaded to the ProjectPythia Google Drive and lives in the Analytics_API folder.

**This credentials file needs to be kept secure**, especially the `private_key` field. **Do NOT share this file.** If you do not have access to our Google Drive and need access to this file, please reach out to the team on discourse or in a community meeting.

The credentials file will have a name similar to `cisl-vast-pythia-{letters and numbers}.json`. This file may be replaced intermittently with a slightly different alphanumeric string for additional security.

One way to ensure that your Python script is using the correct credentials file is to read it as a dictionary and pass that into your API client at the beginning of your script.

```
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest

with open('{credentials-file-path}') as json_file:
   credentials_dict = json.load(json_file)

client = BetaAnalyticsDataClient.from_service_account_info(credentials_dict)
```

Recommended and commonly needed import statements are also shown at the script beginning.

### Making a request

Below is a sample function for calling an Analytics API request.

```
def _run_analytics_request(property_id):
    request = RunReportRequest(
        property=f'properties/{property_id}',
        dimensions=[Dimension(name='date')],
        metrics=[Metric(name='activeUsers')],
        date_ranges=[DateRange(start_date='2024-01-01', end_date='today')],
    )
    response = client.run_report(request)
    return response
```

This function demonstrates how to format your `RunReportRequest()` arguments, notably the `dimensions` and `metrics` fields, as well as the expected date formatting in `date_ranges`.

This [Google Analytics API Schema](https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema) documentation lists all of the available dimension and metric keys that can be passed into your request.

`property_id` is a 9-digit number associated with the project you are interested in. This number can be found on the Analytics project page. For Project Pythia, our three different property IDs are:
```
PORTAL_ID = '266784902'
FOUNDATIONS_ID = '281776420'
COOKBOOKS_ID = '324070631'
```

### Working with your request output

Your Google Analytics response is formatted in a series of rows that each have the key `dimension_value` and `metric_value`. You may find it easier to work with your data in a dictionary or tuple. For the single dimension of "date" and metric of "activeUsers" as specified in our example function, here is what your data manipulation may look like before you can carry out additional analysis.

```
dates=[]
users=[]
for row in response.rows:
    date_str = row.dimension_values[0].value
    date = datetime.datetime.strptime(date_str, '%Y%m%d')
    dates.append(date)
    users.append(int(row.metric_values[0].value))

dates, users =  zip(*sorted(zip(dates, user_counts), key=lambda x: x[0]))
```

One thing to note is that your Analytics response rows are not automatically chronological, so in this example we zipped our sorted tuple to ensure that the dates are in the expected order.
