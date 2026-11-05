---
title: "Rebuilding the Pythia Gallery on shared MyST tooling"
subtitle: A few infrastructure improvements from the 2026 Cookoff
date: 2026-06-23
author: choldgraf
description: How we used the Pythia Cookoff hackathon to rebuild the Cookbook Gallery and blog on reusable MyST tooling, and improve the clinder project along the way.
tags: ["gallery", "myst", "hackathon"]
---

The [Project Pythia Cookbook Gallery](https://cookbooks.projectpythia.org/) is a central resource that Pythia uses to show off all the cookbooks its projects have created. Under the hood, it uses the [MyST Document Engine](https://mystmd.org) to execute and build each cookbook.

```{figure} images/gallery-new.png
The redesigned Cookbook Gallery, with a search bar and consistent cards.
```

Previously, the gallery ran on a collection of custom scripts and MyST plugins.
This year at the [2026 Pythia Cookoff](https://projectpythia.org/pythia-cookoff-2026/) at NCAR, we used some hackathon time to rebuild it on upstream tooling that is more sustainable and re-usable across projects.
Here's a quick summary of what we did:

## Improving the gallery with a new myst-listing plugin

The old gallery ran on a custom MyST extension that collected cookbook metadata from the Pythia organization and displayed it in a gallery of images.
We decided to improve the UI and UX of this experience, and turn it into a Jupyter Book plugin in the new [`myst-contrib`](https://github.com/myst-contrib) GitHub organization.

You can find the new [`myst-listing` plugin here](https://contrib.mystmd.org/myst-listing). It defines an experimental three-step process for **collecting** sources of content and information, **transforming** them by adding extra metadata, and **displaying** them in a variety of output styles.
This is an experimental plugin, but we hope others can start to try it out and make improvements as they go along.

Along the way, we switched the cookbooks gallery to use this new `myst-listing` plugin. To do this, we removed all of the old custom plugin code and replaced it with a [lightweight MyST plugin](https://github.com/ProjectPythia/cookbook-gallery/blob/main/src/pythia_gallery.py) that simply collects cookbook metadata from each repository, and uses the `myst-listing` plugin to render it into a nice gallery.
We added the `searchfilter` plugin as well to get a nice search bar at the top.

Check out [`cookbooks.projectpythia.org`](https://cookbooks.projectpythia.org) and the PR that implements this: https://github.com/ProjectPythia/cookbook-gallery/pull/33.

## A new blog setup with the listing plugin

We also decided to re-build the blog on the same `myst-listing` plugin.
This was a way to test whether the plugin we'd created above could generalize to a new kind of use-case.
The blog also used to be a collection of custom scripts and plugin code, and it's now replaced with a simple call to `:::{listing}`.
Check out the PR that implements this: https://github.com/ProjectPythia/projectpythia.github.io/pull/582.

## Executing cookbooks with remote kernels on Binder

The week also gave us a reason to push on [`clinder`](https://2i2c-org.github.io/clinder/), our BinderHub CLI and GitHub Action for executing cookbooks with a remote kernel in the cloud.
It lets a MyST or Jupyter Book build execute its notebooks on mybinder.org in CI instead of the runner, which is a nice fit for cookbook-style content.
We added a documentation site, preview deploys, and tests on pull requests, so it's easier to pick up for your own builds.

You can find a PR demoing this new functionality in [`pythia-foundations` PR #655](https://github.com/ProjectPythia/pythia-foundations/pull/655), where the build comment links to a [working preview of the book](https://ProjectPythia.github.io/pythia-foundations/_preview/655) executed on Binder.

## Learn More
- [Cookbook Gallery PR #33](https://github.com/ProjectPythia/cookbook-gallery/pull/33)
- [Pythia blog and landing page PR #582](https://github.com/ProjectPythia/projectpythia.github.io/pull/582)
- [`myst-listing` plugin docs](https://contrib.mystmd.org/myst-listing)
- [`clinder` documentation](https://2i2c-org.github.io/clinder/)
