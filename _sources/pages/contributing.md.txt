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

When testing new content is important to build and view the site. Read the Docs automatically builds the site for you when each Pull Request is checked. You can also build it locally on your machine.

### To view the Read the Docs autobuild

Once a Pull Request has passed all tests, including the Read the Docs build, you can click "Details" of the check that says, "docs/readthedocs.org:projectpythia - Read the Docs build succeeded!" to launch a new tab with a build of the Project Pythia site. (You may have to click "Show all checks" for this to be displayed.)

![Checks](../_static/images/ReadtheDocsAutobuild.png)

### To build and view the site locally

- Fork the [source repository](https://github.com/ProjectPythia/projectpythia.github.io) on GitHub
- Make a local clone of the repository on your machine
  ```bash
  git clone git@github.com:USERNAME/projectpythia.github.io.git
  # or
  git clone https://github.com/USERNAME/projectpythia.github.io.git
  ```
- In your favorite terminal, navigate to the `content` directory of the source repository
  ```bash
  cd projectpythia.github.io/content
  ```
- Use [conda](https://docs.conda.io/) to set up a build environment:
  ```bash
  conda env create -f ../ci/environment.yml
  conda activate pythia
  ```
- Build the site locally using Sphinx (which you just installed in the `pythia` environment, along with all necessary dependencies):
  ```bash
  make html
  ```
- The newly rendered site is now available in `content/_build/html/index.html`.
  Open with your web browser, or from the terminal:
  ```bash
  open _build/html/index.html
  ```
- When you're done, you can deactivate the dedicated build environment with
  ```bash
  conda deactivate
  ```
- You can re-activate the `pythia` conda environment at any time with `conda activate pythia`.
