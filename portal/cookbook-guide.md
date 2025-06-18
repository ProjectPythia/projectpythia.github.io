# Cookbook Contributor's Guide

Project Pythia Cookbooks are collections of more advanced and domain-specific example
workflows building on top of [Pythia Foundations](https://foundations.projectpythia.org/landing-page.html).
They are [geoscience](https://en.wikipedia.org/wiki/Earth_science)-focused
and should direct the reader towards the Foundations material for any required
background knowledge.

The following is a step-by-step guide to creating a new Cookbook and getting it hosted on the [Project Pythia Cookbook Gallery](https://cookbooks.projectpythia.org).

Before you begin, ask yourself if the content you are developing for a cookbook would be better suited as an addition to an existing cookbook. The best place to discuss cookbook ideas is the [Project Pythia category of the Pangeo Discourse](https://discourse.pangeo.io/c/education/project-pythia/60).

```{note}
These instructions assume that your goal is to contribute a new Cookbook to the community-maintained collection housed on the [Pythia Cookbook Gallery](https://cookbooks.projectpythia.org).

Using the Pythia Cookbook template to create reproducible documents housed elsewhere is definitely possible! But we don't focus on that use case in this guide.
```

If you're not looking to create a _new_ Cookbook, but rather looking for guidance on contributing to _existing_ Cookbooks, first make sure you're comfortable with the [GitHub forking workflow](https://foundations.projectpythia.org/foundations/github/github-workflows.html#forking-workflow), then take a look at the section below on "Pull Requests and previews".

## Data access

Before developing your cookbook, you should consider how it will access the data you plan to use. In loose order of preference, we recommend the following:

1. Rely on data that is already freely available and accessible with tools in the ecosystem. Point to Foundations or other cookbooks for tool how-to guides if needed. Examples include the [CMIP6 Cookbook](https://projectpythia.org/cmip6-cookbook/) and the [CESM LENS on AWS Cookbook](https://projectpythia.org/cesm-lens-aws-cookbook/)
1. Focus on representative subsets of data that can be packaged alongside the cookbook in-repo. An example is the [Landsat ML Cookbook](https://projectpythia.org/landsat-ml-cookbook/README.html)
1. Discuss your larger data storage needs with the Pythia team. We are currently experimenting with cloud object storage for Cookbooks via NSF JetStream2.
1. Provide the tools and/or clear documentation for accessing the data that you have stored somewhere else

## Use the template

1. If you don't already have a GitHub account, create one by following the [Getting Started with GitHub guide](https://foundations.projectpythia.org/foundations/getting-started-github.html)
1. On the [Cookbook Template repository](https://github.com/ProjectPythia/cookbook-template), click "Use this template &rarr; Create a new repository"
1. Choose "Include all branches".
1. Give your repository a descriptive name followed by `-cookbook` (e.g., `hydrology-cookbook`, `hpc-cookbook`, `cesm-cookbook`) and a description
1. Create the repository. Your browser will be directed to the newly created repository under your GitHub account
1. Under Settings &rarr; Pages, ensure that GitHub Pages is enabled by checking that `Branch` is set to "gh-pages", and the folder set to "gh-pages/(root)". If it is not, change the Branch from "None" to "gh-pages/(root)" and click "Save"
1. Under Settings &rarr; Actions &rarr; General, make sure that "Read and write permissions" is selected. <img width="901" alt="Screenshot 2023-01-13 at 3 12 47 PM" src="https://user-images.githubusercontent.com/26660300/212428991-cd0ae2f0-73ca-40d8-b983-f122359463aa.png">

Your cookbook is now ready to have content added!

```{note}
In the rest of this guide, we assume that you are familiar with the basics of using git and GitHub. If not, we strongly recommend reading through our [GitHub tutorials in Foundations](https://foundations.projectpythia.org/foundations/getting-started-github.html).
```

## Transfer your cookbook repo to the ProjectPythia organization

In order for your Cookbook to be included in the Gallery, the source repository needs to be housed within the [Project Pythia GitHub organization](https://github.com/ProjectPythia).

You can keep your repository in your personal GitHub space while you're developing your content if that works better for you. Repository ownership can be transferred at any time.

However, we recommend transferring to the Pythia organization early, for a few reasons:
- Fewer settings to tweak later
- Easier to get help from the Pythia infrastructure team
- Encourages collaboration

```{note}
You're still in control! You will always retain write access to your Cookbook repository even after transfering ownership to the Pythia organization.

Also, _don't worry about breaking anything!_ Your repo will not affect any other Project Pythia content until you initiate the request to list it on the [Cookbook Gallery](https://cookbooks.projectpythia.org) (see below...)
```

### Steps to transfer the repository

1. [Contact the Pythia team via the Pangeo Discourse](https://discourse.pangeo.io/c/education/project-pythia/60) (or otherwise) to let us know about your cookbook.
1. You will get an invitation to join the [ProjectPythia organization](https://github.com/ProjectPythia).
1. Accept the GitHub invitation. _Welcome to the team!_
1. Once you are a member of the organization, navigate to the Settings of your cookbook repository and scroll down to the **Danger Zone**.
1. Click "Transfer".
1. Select or type "ProjectPythia", confirm, and transfer.
1. When prompted about which teams to give access to, select "core". _This will enable the Pythia maintenance team to have full access to your repository._

Once you have successfully transferred the repository, you'll most likely want to make a [personal fork and a local clone of the repository](https://foundations.projectpythia.org/foundations/github/github-cloning-forking.html) so that you can continue to develop and collaborate on the Cookbook via the [forking workflow](https://foundations.projectpythia.org/foundations/github/github-workflows.html#forking-workflow).

## Customize the paths in your repository

Whether the repository lives in your personal GitHub space or on the ProjectPythia organization, there are several paths and links in the repository code that need to be updated to reflect the current home of your cookbook source. This step is necessary to ensure that the cookbook building and publishing infrastructure works as intended.

Fortunately this is quick and easy. Just run our custom GitHub action called `trigger-replace-links`: Navigate to "Actions" &rarr; "trigger-replace-links" &rarr; "Run workflow".

## Set up the computational environment

You'll most likely want to do your edits in a [local clone of the repository](https://foundations.projectpythia.org/foundations/github/github-cloning-forking.html) on your laptop or wherever your are running your notebooks.

### Customizing your environment file

1. Within `environment.yml` (in the root of the repository), change `name` from `cookbook-dev` to `<your-cookbook-name>-dev` (e.g. `cesm-cookbook-dev`) and add all required libraries and other dependencies under `dependencies:`. Commit the changes.
1. Create the [conda environment](https://foundations.projectpythia.org/foundations/conda.html) with `conda env create -f environment.yml`. If it crashes, try running `conda config --set channel_priority strict`
1. Activate your environment with `conda activate <env-name>`

You're now ready to create and run awesome notebooks.

### Customizing your GitHub actions

Your repository includes automation for building and publishing your Cookbook, powered by [GitHub Actions](https://docs.github.com/en/actions). Now that you have created a custom name for your conda environment (`<your-cookbook-name>-dev`), you need to edit three files found in the `.github/workflows` section of your repo:
- `.github/workflows/nightly-build.yaml`
- `.github/workflows/publish-book.yaml`
- `.github/workflows/trigger-book-build.yaml`

In each of these files, in the field called `environment_name:`, replace  `cookbook-dev` with the name you used in your `environment.yml` file (probably `<your-cookbook-name>-dev`). Commit these changes.

```{note}
If these workflow files look mysterious and you don't know anything about how GitHub Actions work, don't worry! The Pythia team will help with any problems that arise with the Cookbook automation.
```

## Develop your cookbook

### Add notebooks

To add content, you should edit (and duplicate as necessary) the notebook template `notebooks/notebook-template.ipynb`. Using this template will help keep your content consistent with the expected Cookbook style.

You can add subfolders to organize your notebook files as necessary. However, the organization of the notebooks within the published book is dictated by the table of contents file `_toc.yml`. _Edit this file to add your chapters._ Take a look at the [`radar-cookbook/_toc.yml`](https://github.com/ProjectPythia/radar-cookbook/blob/main/_toc.yml) for example syntax, or consult the [JupyterBook documentation](https://jupyterbook.org/en/stable/structure/toc.html).

### Customize your home page

The file `README.md` serves as the homepage of your Cookbook, so it should be descriptive. Edit this file as appropriate, following guidance in the file itself.

### Build your Cookbook locally

You should be able to build your new Cookbook on your local machine by running this command from the root of the repository:
```
jupyter-book build .
```
from the root of your repository. This will execute all your notebooks and package them into a book styled with the Pythia theme.

If the build is successful, you should be able to preview the result in a web browser by running
```
open _build/html/index.html
```

### Strip output from your notebooks before committing

Wherever feasible, we recommend only committing bare, unexecuted notebooks into your Cookbook repository. There are a few reasons:
- The notebooks are executed automatically each time the book is built
- Pre-existing output in the notebooks will have no effect on the published book
- Better reproducibility of your content
- The repo stays cleaner and leaner. Diffs of notebook changes are easier to interpret.

To strip a notebook, in a Jupyter Lab session, go to "Kernel" &rarr; "Restart Kernel and Clear Output of All Cells...". Save your notebook, then commit.

You're ready to push content up to GitHub and trigger the automated publishing pipeline.

## Deploying your Cookbook

Pythia Cookbooks are not just collections of notebooks! They are backed by GitHub-based automation that handles building, testing, previewing, and publishing the books online.

### About the publishing pipeline

Any time you push new content to the `main` branch of your Cookbook repo, actions are triggered that do the following:
- Create an up-to-date build environment using your `environment.yml` file
- Execute all the notebooks in that environment
- Package the book into a styled website
- Check all the links in the website to make sure they are valid
- Deploy the styled website so it's visible to the world

### Where is my book?

The URL of your published book will depend on where the source repository is housed.
- If the repo is in the [Project Pythia organization](https://github.com/ProjectPythia), the book is published to `https://projectpythia.org/[YOUR_COOKBOOK_REPO_NAME]/`
- If the repo is in your personal GitHub space, the book is published to `https://[YOUR_GITHUB_USERNAME].github.io/[YOUR_COOKBOOK_REPO_NAME]/`

Here's a handy trick for finding your published book:
- On the home page of your GitHub repo, look for the "About" section in the right-hand side bar.
- Click the "gear" icon next to "About"
- Select the checkbox "Use your GitHub Pages website".
- Is that checkbox missing? That likely means you're looking at the "About" section of your _personal fork_, not the upstream fork. Navigate back to `https://github.com/ProjectPythia/[YOUR_COOKBOOK_REPO_NAME]/` and look for it there.

The link to your published book will then be displayed on the home page of the repo.

```{note}
If you have transfered your repository to the ProjectPythia organization and also made a personal fork, the publishing pipeline automation will _only run on the upstream fork on the ProjectPythia organization_ so there's only one copy of the "published" book.

It's possible to enable the workflows on your personal fork, but usually unnecessary if you preview your work via Pull Requests (see next section)!
```

### Pull Requests and previews

Collaboration on Cookbooks is best done via [Pull Requests](https://foundations.projectpythia.org/foundations/github/github-pull-request.html). Every PR on a Cookbook repository will trigger a "Preview" version of our publishing pipeline. The entire book is re-built from the updated source and the preview site is hosted at a temporary online location. This way, the team can safely see what the end product will look like after the PR is merged.

The only difference between the "preview" pipeline and the regular publishing pipeline is the URL to which the rendered website is deployed. A temporary preview location is used, leaving the main book untouched until the PR is merged.

To propose changes to a Cookbook, or even just to test something out temporarily, follow the [forking workflow](https://foundations.projectpythia.org/foundations/github/github-workflows.html#forking-workflow): make changes on a feature branch of your personal fork, and open a Pull Request from that branch to the main branch of the upstream fork. This will trigger the preview.

A link to the preview will appear as a comment on the Pull Request once the publishing actions are complete. _If the link shows up but you get a 404 error when you click on it the first time, just wait a few minutes! There are some lags before the preview is fully deployed._

Not satisfied? Keep making changes! Every new push to the feature branch on your personal fork will trigger another rebuild, and an updated preview. The preview will be deleted if and when the PR is closed or merged.

### Building on the Pythia Binder

```{note}
By default, notebooks are executed on the free GitHub Actions service. This works fine for most lightweight Cookbooks. If your book is building and publishing succesfully, you can safely ignore this section!
```

For Cookbooks with substantial compute requirements, you have the option of routing notebook execution to a specialized Binder service maintained by the Project Pythia team.

Here's how:
- Edit your `_config.yml` in the root of your repo.
- Change the field `execute_notebooks` from `cache` to `binder`.
- Commit that change and open a Pull Request to your main branch.
- That will trigger a build and preview as usual, but the notebook execution will happen on the Binder.
- If all is well, merge the changes, and all further builds will work this way.

```{note}
The Binder uses your `environment.yml` file to create an image of an execution environment, which is stored for reuse. The time to execute your notebooks can vary, depending on whether the Binder needs to build a new image or not.
```

## Publish your Cookbook on the Pythia Gallery

Once you're happy with your content and your Cookbook is building and deploying properly, it's time to think about submitting it for inclusion in the [Cookbook Gallery](https://cookbooks.projectpythia.org/)!

```{note}
Cookbooks don't need to be "finished" in order to accepted in the Gallery! Cookbooks are typically accepted so long as they run cleanly, are free of obvious errors, and have some relevant new content.

Cookbooks are meant to be living documents. We encourage authors to open GitHub issues to track progress on adding and updating content.
```

At this stage, there are a few more steps to get things ready to go.

### Authorship and the `CITATION.cff` file

Cookbooks are scholarly objects. As part of the publication process, your Cookbook will get a citable DOI (via [Zenodo](https://zenodo.org)). Just as for journal publications, you need to make decisions about who gets credited for authorship.

This information is managed manually through the file `CITATION.cff` in the root of your repository. This will determine the names displayed on your card in the [gallery](https://cookbooks.projectpythia.org/) as well as your DOI-based citation.

Edit `CITATION.cff` as follows:

- If you haven't already, _remove the people already listed in this file_. These are the credited authors of the [Cookbook Template](https://github.com/ProjectPythia/cookbook-template) only, and they should not be included in your author list (unless one of them also happens to be a content author for your book).
- Set your Cookbook title
- Write a short description / abstract (this will also appear on the [gallery](https://cookbooks.projectpythia.org/))
- Include names of all content authors
  - ORCID and other metadata for each author is optional but helpful
- Under the `name:` field, change "Cookbook Template contributors" to "[Your Cookbook Name] contributors"

```{note}
GitHub automatically tracks all contributions to your repository. The folks who help with infrastructure fixes, content reviews, etc., are considered "contributors" but not primary authors. We include the "contributors" as a single group in `CITATION.cff` to acknowledge this!
```

### Gallery tags

The file `_gallery_info.yml` determines how your Cookbook will be findable on the [gallery](https://cookbooks.projectpythia.org/). Edit this file with the following:

- Replace `thumbnail.png` with your own image (which will appear on your gallery card)
- Edit the tags under `domains` and `packages` as appropriate. Check out the existing filters on the [gallery page](https://cookbooks.projectpythia.org/) to get a sense of how these are used.

### Generate a DOI

Once all the above steps are complete and your `CITATION.cff` file is correct, you are ready to "release" a tagged version of your book and generate your first DOI. We've tried to make this as painless as possible, but there are a few more steps to take initially.

As always, reach out to a Pythia team member for help with any of these steps!

1. Go to [zenodo.org](https://zenodo.org) and log in. If you have never used Zenodo, you will need to create an account. We recommend authenticating through GitHub.
1. Once logged in to Zenodo, under "My account", click on "GitHub".
1. You will see a long list of GitHub repositories, both your personal repos as well as the ProjectPythia repos.
1. Find your Cookbook repository (which needs to be housed in the ProjectPythia organization at this point), and toggle the "On" switch.
1. Now, leave Zenodo and go back to GitHub
1. Make a new release of your Cookbook repository! This is on the right nav side of the page from your code-view in the repository.
1. The DOI will now be generated automatically. The DOI badge on your homepage should link to the new archive that was just created on Zenodo.

### Initiate the Cookbook review process

If you haven't already, now is a great time to [contact the Project Pythia team](https://discourse.pangeo.io/c/education/project-pythia/60) to let them know about your new Cookbook. You will be assigned a Cookbook advocate from the Pythia maintenance team.
They will open an issue on your Cookbook repository with the [Cookbook Checklist](cookbook-tasklist.md) for you to document your completion of the above process, plus a few more GitHub-specific steps.
Once you complete this process, your Cookbook will be ready for review and publication!

### Submit your Cookbook to the Gallery

Click the button below to request addition of your Cookbook to the [Project Pythia Cookbook Gallery](https://cookbooks.projectpythia.org).

<span class="d-flex justify-content-center py-4">
    <a href="https://github.com/ProjectPythia/cookbook-gallery/issues/new?assignees=ProjectPythia%2Feducation&labels=content%2Ccookbook-gallery-submission&template=update-cookbook-gallery.yaml&title=Update+Gallery+with+new+Cookbook" role="button" class="btn btn-light btn-lg" style="display: flex; align-items: center; font-weight: 600; text-decoration: none;">
        Submit a new Cookbook
    </a>
</span>

1. Click the above button, or use this link to the [new cookbook PR template](https://github.com/ProjectPythia/cookbook-gallery/issues/new?assignees=ProjectPythia%2Feducation&labels=content%2Ccookbook-gallery-submission&template=update-cookbook-gallery.yaml&title=Update+Gallery+with+new+Cookbook).
1. Add the root name of your cookbook repository (e.g., just "cesm-cookbook", not the whole URL) and any other information you'd like the team to know.
1. The Pythia team will take a look at your content, and work with you on any necessary updates and fixes.

__*THANK YOU FOR YOUR AMAZING CONTRIBUTION TO THIS COMMUNITY RESOURCE!*__
