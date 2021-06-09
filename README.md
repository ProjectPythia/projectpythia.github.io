# Project Pythia Portal

![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/NCAR/pythia-portal/deploy-site/main?logo=github&style=for-the-badge)

This is the source repository for the [Project Pythia portal](https://projectpythia.github.io).
The portal site is built with [sphinx](https://www.sphinx-doc.org/).

To build the site locally (e.g. for testing new content),
use [conda](https://docs.conda.io/) to set up a build environment with all dependencies.

First, make a local clone of this source repository on your machine. For example:

```
git clone https://github.com/ProjectPythia/projectpythia.github.io.git
```

Then, change working directories to the local repository's `content` directory:

```
cd projectpythia.github.io/content
```

Set up your a conda environment:

```
conda env create -f ../ci/environment.yml
conda activate pythia
```

You can then build the site with:

```
make html
```

After building the site it may be possible to preview the portal in your web browser by simply opening the `index.html` file:

```
open _build/html/index.html
```

However, many of the links will not work. For all of the links found in the portal to work properly, you'll need to set up a local testing server. This can be done with Python's http.server by running the following command from within the `content` directory:

```
python -m http.server --directory _build/html/
```

and then pointing your browser at the URL: `localhost:8000`.

More information on setting up a local test server is available from [here](https://developer.mozilla.org/en-US/docs/Learn/Common_questions/set_up_a_local_testing_server)


You can find more details in the [Contributor's Guide](https://projectpythia.org/pages/contributing.html).
