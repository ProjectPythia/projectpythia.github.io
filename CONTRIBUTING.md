# Pythia Portal contributor's guide

This document contains information specific to contributing to the
Project Pythia Portal.  Please first refer to [Pythia Contributor's
Guide](https://projectpythia.org/pages/contributing.html) for overall
contribution guidelines (such as detailed description of Project
Pythia structure, forking, repository cloning, branching, etc.).

## Instructions for building the portal site

The portal site is built with [Sphinx](https://www.sphinx-doc.org/).

When testing new content is important to build and view the site. Read the Docs automatically builds the site for you when each Pull Request is checked. You can also build it locally on your machine.


### Building the site

- After checking out a local copy of the site, in your favorite terminal, navigate to the `content` directory of the source repository
  ```bash
  cd projectpythia.github.io/content
  ```
- Use [conda](https://docs.conda.io/) to set up a build environment:
  ``` bash
  conda env create -f ../ci/environment.yml
  conda activate pythia
  ```
- Build the site locally using Sphinx (which you just installed in the `pythia` environment, along with all necessary dependencies):
  ``` bash
  make html
  ```
- The newly rendered site is now available in `content/_build/html/index.html`.
Open with your web browser, or from the terminal:
  ``` bash
  open _build/html/index.html
  ```
- When you're done, you can deactivate the dedicated build environment with
  ``` bash
  conda deactivate
  ```
- You can re-activate the `pythia` conda environment at any time with `conda activate pythia`.

### To view the Read the Docs autobuild

Once a Pull Request has passed all tests, including the Read the Docs build, you can click "Details" of the check that says, "docs/readthedocs.org:projectpythia - Read the Docs build succeeded!" to launch a new tab with a build of the Project Pythia site. (You may have to click "Show all checks" for this to be displayed.)

![Checks](../_static/images/ReadtheDocsAutobuild.png)
