# Pythia Portal contributor's guide

This document contains information specific to contributing to the
Project Pythia Portal. Please first refer to [Pythia Contributor's
Guide](https://projectpythia.org/contributing.html) for overall
contribution guidelines (such as detailed description of Project
Pythia structure, forking, repository cloning, branching, etc.).

## Instructions for adding a blog post
Within the `portal/posts/` folder add your `.md` blog file with the following heading:

```
---

date: YYYY-MM-DD
author: First Last
tags: [sample-tag]
---
```

The post will automatically be recognized and displayed when you build the portal site.

## Instructions for building the portal site

The portal site is built with [Sphinx](https://www.sphinx-doc.org/).

When testing new content it is important to build and view the site. Read the Docs automatically builds the site for you when each Pull Request is checked. However, you can also build it locally on your machine following the instructions
below.

### Building the site

After checking out a local copy of the site, in your favorite terminal, navigate to the `portal` directory of the source repository

```bash
cd projectpythia.github.io/portal
```

Use [conda](https://docs.conda.io/) to set up a build environment:

```bash
conda env update -f ../environment.yml
```

This will create the dev environment (`pythia`). If you have previously created the environment, running this command will add any new packages that have since been added to the `environment.yml` file.

It's a good idea to also keep the *versions* of each package in the `pythia` environment up to date by doing:

```bash
conda activate pythia
conda update --all
```

#### Install `pre-commit` hooks

This repository includes `pre-commit` hooks (defined in
`.pre-commit-config.yaml`). To activate/install these pre-commit
hooks, run:

```bash
conda activate pythia
pre-commit install
```

Setting up the environment is typically a one-time step.

_NOTE_: The `pre-commit` package is already installed via the `pythia` conda environment.

#### Building the book locally

Build the site locally using Sphinx (which you just installed in the `pythia` environment, along with all necessary dependencies):

```bash
make html
```

If this step fails and you have not updated your conda environment recently, try updating with `conda env update -f ../environment.yml` and `conda update --all` as described above.

The newly rendered site is now available in `portal/_build/html/index.html`.
Open with your web browser, or from the terminal:

```bash
open _build/html/index.html
`````

However, many of the links will not work. For all of the links
found in the portal to work properly, you'll need to set up a local
testing server. This can be done with Python's http.server by running
the following command from within the `portal` directory:

```bash
python -m http.server --directory _build/html/
```

and then pointing your browser at the URL: localhost:8000.

More information on setting up a local test server is available from [here](https://developer.mozilla.org/en-US/docs/Learn/Common_questions/set_up_a_local_testing_server)

When you're done, you can deactivate the dedicated build environment with

```bash
conda deactivate
```

You can re-activate the `pythia` conda environment at any time with `conda activate pythia`. You may also want to update each package in the activated environment to their latest versions by doing

```bash
conda activate pythia
conda update --all
```

### Preview the built site on Netlify

Once a pull request has passed all tests, including the `preview-site` check, the GitHub bot will post a comment with a preview link on the pull request. You can click on the link to launch a new tab with a build of the Project Pythia site.

![CI-check](/portal/_static/images/deploy-site-CI-check.png)

![Netlify Preview](/portal/_static/images/netlify-preview.png)


## Instructions for intacting with the Google Analytics API

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

One way to ensure that your Python script is using the correct credentials file is to read it as a dictionary and pass that into your API client at the begging of your script.

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
