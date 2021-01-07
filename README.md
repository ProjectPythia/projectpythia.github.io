# Project Pythia Portal

![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/NCAR/pythia-portal/deploy-site/main?logo=github&style=for-the-badge)

This is the source repository for the [Project Pythia portal](https://projectpythia.github.io).
The portal site is built with [sphinx](https://www.sphinx-doc.org/).

To build the site locally (e.g. for testing new content),
use [conda](https://docs.conda.io/) to set up a build environment with all dependencies.

First, make a local clone of this source repository on your machine.
Then, from the `content` directory of the source repository, do this:
```
conda env create -f ci/environment.yml
conda activate pythia
```

You can then build the site:
```
make html
```
and view the built site in your web browser with
```
open _build/html/index.html
```
