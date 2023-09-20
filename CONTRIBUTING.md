# Pythia Portal contributor's guide

This document contains information specific to contributing to the
Project Pythia Portal. Please first refer to [Pythia Contributor's
Guide](https://projectpythia.org/contributing.html) for overall
contribution guidelines (such as detailed description of Project
Pythia structure, forking, repository cloning, branching, etc.).

## Instructions for adding a blog post

We use [Sphinx ABblog](https://ablog.readthedocs.io/en/stable/) to add blog posts to our site.

Within the `portal/posts/` folder add your `.md` blog file with the following heading:

```
---
blogpost: true
date: MON DD, YYYY
author: First Last
tags: sample-tag
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
