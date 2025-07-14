---
title: Reflections on MyST-ification
subtitle: Project Pythia’s transition to MyST and JupyterBook2 architecture
date: 2025-07-10
authors: [jukent, brian-rose, dcamron, kafitzgerald]
tags: [myst]
---

Project Pythia recently transitioned from a [Sphinx-based JupyterBook](https://jupyterbook.org/en/stable/intro.html) architecture to using [MyST Markdown](https://mystmd.org/), which serves as the foundation for the upcoming [JupyterBook 2](https://next.jupyterbook.org/)!

## Our Motivation for MyST
We began the process of transitioning to MyST in the summer of 2024 at the annual [Project Pythia Cook-off hackathon](https://projectpythia.org/posts/2025/new-cookbooks). At that event, members of the MyST team demonstrated the current [alpha-version of the technology](https://executablebooks.org/en/latest/blog/2024-06-14-project-pythia-mystmd/) and coached us through the boilerplate code necessary to make some of our key resources build with MyST.

The new MyST architecture was very appealing for several reasons:
- **Sustainability**: Our current Sphinx-based architecture was becoming clunky and hard to maintain as members joined or left the project, and required too much boilerplate code in individual cookbook repos which presented a barrier to would-be new contributors. MyST offered a much more streamlined alternative to keep our community project growing.
- **Staying on the leading edge of best practices**: We are an open-source community resource that teaches open-source coding practices, so it’s important that our own sites continue to be useful models for the broader community.
- **Making cookbooks better!** A lot of the new functionality in MyST is really well suited to the cookbooks, including things like [cross-referencing](https://mystmd.org/guide/cross-references) and [embedding content](Embed & Include Content - MyST Markdown) and automated [bibliographies](https://mystmd.org/guide/citations).
- **Cross-pollination with the core developers!** Having the MyST developers invested in our use-case as a demo as they learn, understand, and develop functionality that will be particularly useful to us (and users that come after) is a really nice feedback loop from both a community and technological stand point.

## MyST for sustainability
### Our aging infrastructure
One example of our maintainability challenge was keeping our bespoke [Pythia-Sphinx theme](https://github.com/ProjectPythia/sphinx-pythia-theme) up-to-date. Upstream dependency updates and cascading syntax changes will always be a concern for the open source community. Combine that with browser default settingschanging since the birth of this project in 2020 (particularly for dark-mode), and there were many HTML and CSS customizations that were no longer displaying as intended. For this reason, we decided to stick as closely to the default [MyST book-theme](https://mystmd.org/guide/website-templates) as serves our purposes. The fewer moving pieces for a new contributor in our open source community to have to be spun up on the better. And with our current collaborations with the MyST team, it’s better to put effort into helping to improve the core tools rather than create unique new customizations.

### Repository sprawl
Another maintainability challenge was propagating changes across many GitHub repositories. Within the [Project Pythia Github organization](https://github.com/ProjectPythia/) we currently have 75 different repositories, the vast majority of which contain some website source under the big trenchcoat masquerading as one single Project Pythia website. Each repository is deployed within the domain, but there are separate repositories for our [home page](https://projectpythia.org/), [Foundations book](https://foundations.projectpythia.org/), [resource](https://projectpythia.org/resource-gallery/) and [Cookbooks galleries](https://cookbooks.projectpythia.org/), and for each individual Cookbook. With the Sphinx infrastructure, while the site theming could be abstracted into its own package, other changes to the site configuration or appearance, specifically of the links included in the top nav-bar or footer, would have to be individually updated in every single repository for consistency. We could update our Cookbook Template repository, but GitHub has no one way of sending those divergent-git-history changes to the various Cookbook repositories that leveraged that template. The MyST [`extends` keyword](https://mystmd.org/guide/frontmatter#composing-myst-yml) in the configuration file allows us to not only abstract theming, but also configuration commands and content. Future changes to the site navbar will only have to be made in one place, and individual Cookbook authors will be able to focus on their own content with much reduced boilerplate!

## Making the Switch
### Getting to yes
Before we could get to the point of “only having to make changes in one place” we had to make a lot of changes in ALL of our repositories. Initially the process was exploratory. We had a separate MyST GitHub organization to host the MyST versions of our home page and galleries. Various team members MyST-ified a Cookbook repository or two just to test the process. Over the fall, winter, and spring we stayed in touch with the MyST devs and helped scope out updates and releases that would meet our needs. Come spring, we faced a decision: Do we complete the transition before or after our [August 2025 Cook-off Hackathon](https://projectpythia.org/pythia-cookoff-2025/)?
Ultimately, we decided to flip the switch, transitioning fully to MyST before the hackathon. Reasons for this decision included: stability for contributors (you wouldn’t want to work on a project for it to immediately become unrecognizable to you afterwards) and fewer newly created repositories to track down that don’t match our [new template](https://github.com/ProjectPythia/cookbook-template). With having everyone at the hackathon working within the MyST ecosystem, we decided to transition incomplete Cookbooks as well as current published ones.

### Mystification of our collaborative workflows
The first task was to adapt the shared GitHub Actions workflows that we rely on for building and deploying all our sites. These unique workflows are a key piece of Pythia’s collaboration infrastructure because they enable rich previews of pull requests rendered through the same machinery that builds the actual sites, so we don’t have to guess what the end product will look like – whether we’re changing website formatting or executable content in notebooks. Adapting the workflows to play well with MyST included changing the default build command[^buildcommand] and some new logic to handle MyST’s `BASE_URL` requirement[^baseurl]. With the mystified collaborative workflows in place we were ready for the big, coordinated push this transition would require.

### Sprint to the finish line
In mid-June, we met over the course of several hack days to tinker, to test, to review each other’s pull requests, and to deploy the new websites. We had a spreadsheet to track our progress that listed 57 repositories (including 52 Cookbooks) that needed to be MyST-ified or cleaned up. Knowing that there were paths that were pointing to the old sandbox “with MyST” GitHub organization, even Cookbooks that were previously transitioned to MyST would need to be combed through to make sure all updated changes were reflected. These changes included adding in the new boilerplate code to leverage MyST, updating all action calls, removing any stale code, and other miscellaneous changes to the README.md files and contribution guides. A typical Cookbook had additions, modifications, and deletions of 12 total files ([example](https://github.com/ProjectPythia/xbatcher-ML-1-cookbook/pull/16/files)), which is a total of over 600 files changed in a day. We could not have completed the process so quickly without the rapid response from the upstream MyST Markdown team.

## Looking Ahead
After the sprint day, continued work went into documentation for the new contribution guides, working with the MyST team to identify bugs and new feature requests, and finishing up various tasks. We are currently working diligently on the footer, which will be manually added to 4 key sites while we wait for a MyST release that allows for the extension of site-parts in the configuration. Other key features we hope to include are: gallery extensions for custom gallery card filtering, custom internal vs external link treatment and checking, and better blog functionality. Even without these features, we are thrilled and proud to have rolled out the new infrastructure and a fresh new look for our websites in advance of our summer Cook-off Hackathon.

We hope you’ll find the Cookbook creation process to be streamlined! **Test out our new architecture at this year’s [Cook-off Hackathon](https://projectpythia.org/pythia-cookoff-2025/)** (August 5-8 at the NSF NCAR Mesa Lab in Boulder). Register by July 20th. Or drop by any of our [open community meetings](https://projectpythia.org/#join-us).

## Attribution
Thanks to everyone who was involved in our sprint day (alphabetical):
- Drew Camron
- Rowan Cockett
- Katelyn FitzGerald
- Robert Ford
- Angus Hollands
- Julia Kent
- Christian Okyere
- Brian Rose
- Kevin Tyle

[^buildcommand]: Our shared [build-book.yaml workflow](https://github.com/ProjectPythia/cookbook-actions/blob/main/.github/workflows/build-book.yaml) accepts an arbitrary build_command input argument to accommodate using different HTML building tools. We switched the default build_command from jupyter-book build . to myst build –execute –html. You can restore previous behavior by explicitly setting the input argument from your workflow file like this:
    ```
    jobs:
    build:
        uses: ProjectPythia/cookbook-actions/.github/workflows/build-book.yaml@main
        with:
            build_command: 'jupyter-book build .'
    ```
    Reach out if this is causing problems!

[^baseurl]: Unlike Sphinx, [MyST needs to know where a site is being deployed at build time](https://mystmd.org/guide/deployment-github-pages#base-url-configuration-for-github-pages). That means we have to pass different arguments depending on whether we are building a preview or the actual site since the previews are deployed to subdirectories of each site’s base URL.
