# Contributor's Guide

## Overview

Project Pythia is an open community, and all contributions are welcome following our [Code of Conduct](code_of_conduct.md).

The source code for the Pythia Portal is [publicly hosted on github](https://github.com/ProjectPythia/projectpythia.github.io).
Contributions to open issues and new Pull Requests are welcome at any time.
Detailed instructions for new users will be posted here in the near future.

In the mean time, if you have links to some open educational content that you would like to include in the portal,
feel free to [open an issue on github](https://github.com/ProjectPythia/projectpythia.github.io/issues)
or contact any member of the [Project Pythia core team](people) directly.

For questions or anything else you would like to share with the [Project Pythia Team](people.md), please reach out to us on our [GitHub Discussions page](https://github.com/ProjectPythia/projectpythia.github.io/discussions).

## Instructions for building the portal site

The portal site is built with [Sphinx](https://www.sphinx-doc.org/).

To build and view the site locally (e.g. for testing new content),
use [conda](https://docs.conda.io/) to set up a build environment with all dependencies:

- Fork the [source repository](https://github.com/ProjectPythia/projectpythia.github.io) on GitHub
- Make a local clone of the repository on your machine
- In your favorite terminal, navigate to the `content` directory of the source repository
- Use [conda](https://docs.conda.io/) to set up a build environment:
```
conda env create -f ../ci/environment.yml
conda activate pythia
```
- Build the site locally using Sphinx (which you just installed in the `pythia` environment, along with all necessary dependencies):
```
make html
```
- The newly rendered site is now available in `content/_build/html/index.html`.
Open with your web browser, or from the terminal:
```
open _build/html/index.html
```
- When you're done, you can deactivate the dedicated build environment with
```
conda deactivate
```
- You can re-activate the `pythia` conda environment at any time with `conda activate pythia`.
