# Cookbook Author Checklist Template

Project Pythia maintainers will provide this checklist to Cookbook authors to help get Cookbooks ready for publication.

```md
**I am your Cookbook advocate, and my GitHub handle is <my-username>. Please tag me in this issue with any problems getting your Cookbook published!**
Once we've marked this entire checklist, [click here to open an issue on ProjectPythia/cookbook-gallery to publish your Cookbook!](https://github.com/ProjectPythia/cookbook-gallery/issues/new?assignees=ProjectPythia%2Feducation&labels=content%2Ccookbook-gallery-submission&projects=&template=update-cookbook-gallery.yaml&title=Update+Gallery+with+new+Cookbook)

---

- [ ] **Confirm you’ve followed the entire Project Pythia [Cookbook Guide](https://projectpythia.org/cookbook-guide.html)**.
Take note especially of the [Develop your cookbook](https://projectpythia.org/cookbook-guide.html#develop-your-cookbook), [Authorship and the CITATION.cff file](https://projectpythia.org/cookbook-guide.html#authorship-and-the-citation-cff-file), and [Gallery tags](https://projectpythia.org/cookbook-guide.html#gallery-tags) sections. **Save the [Generate a DOI](https://projectpythia.org/cookbook-guide.html#generate-a-doi) step as the last step of this checklist.**
- [ ] **Confirm that the individual notebooks within your Cookbook adhere to the [notebook template](https://github.com/ProjectPythia/cookbook-template/blob/main/notebooks/notebook-template.ipynb)**.
If the template does not fit your Cookbook’s needs, that’s fine too! Simply let us know here in this issue.
- [ ] **Finalize your Cookbook repository name.**
We generally encourage the `<content>-cookbook` name structure.
- [ ] **Finalize your environment.yml.**
Specify the minimum number of packages needed to reproduce your content. Document any necessary conflicts and pinned package versions in an issue. In your Cookbook README or a content preamble, describe any unique dependencies handled outside the conda environment.
- [ ] **Sufficiently document your code** with markdown narrative text, supplementary media and references, and citations.
Declare any necessary prerequisite learning for each notebook at the top; these can be materials within your Cookbook, within other Cookbooks, or outside Project Pythia altogether.
- [ ] **Review whether your Cookbook needs an Appendix** of terms, definitions, or concepts.
Additionally, should your Cookbook reference other Cookbooks and learning materials to support your content? Could supporting content be added as updates to Foundations or other Cookbooks benefit your Cookbook?
- [ ] **Execute the `trigger-replace-links` action provided to your Cookbook.**
This will update any links to the Cookbook template to refer to your finalized repository name. See ProjectPythia/cookbook-template#183 for manual references to these links if needed.
    - Click the Actions tab for your repository.
    ![GitHub Actions tab link](https://raw.githubusercontent.com/ProjectPythia/projectpythia.github.io/main/portal/_static/images/1-actions.png "Actions Tab")
    - Highlight the `trigger-replace-links` action in the workflows sidebar.
    ![Sidebar list of workflows in GitHub Actions](https://raw.githubusercontent.com/ProjectPythia/projectpythia.github.io/main/portal/_static/images/2-actions-list.png "List of Workflows")
    - On the right-hand side of the page, Run workflow > on Branch: Main.
    ![Prompt for manually running the workflow](https://raw.githubusercontent.com/ProjectPythia/projectpythia.github.io/main/portal/_static/images/3-run-workflow.png "Run Workflow prompt")
- [ ] **Fill in all template sections of your README**.
This will serve as your Cookbook homepage
    - [ ] Title
    - [ ] Cookbook description (brief, under title)
    - [ ] Cookbook Motivation - use this as an opportunity to tell us how your Cookbook fits in the broader learning ecosystem. Who should use this book? Why is it needed? Where does its content begin and end relative to existing resources?
    - [ ] Structure - this section is an optional roadmap for Cookbooks with more complicated structure. If you only have one main body of content that progresses linearly, you can leave this out.
- [ ] **Confirm that your Cookbook is successfully building and publishing via GitHub Actions.**
This can be seen in individual Pull Requests as green checkmarks ✅ for important automation, especially the trigger-book-build action. You can also view a historical list of any of these Actions in the Actions tab at the top of your Cookbook repository. Check out nightly-build and trigger-book-build of PRs, then the build/build jobs to identify code errors. Please comment in this thread if you have issues identifying the source of any build and publishing failures your Cookbook has. Common failures include
    - Incorrectly specified environment.yml
    - trigger-link-check will fail if links in your content can not be resolved. We can help ignore links that are broken even if they work on manual clicks.
    - Code errors in your notebooks themselves
- [ ] **Identify a Maintainer team via GitHub handle(s) in this thread.**
This can be one or more people with availability to check in on this Cookbook, issue fixes to broken content, or with a vision for the future development of the Cookbook. This is typically (but not necessarily) one of the primary authors of the Cookbook.
- [ ] **Link your Cookbook repo to Zenodo for DOI generation**
Follow steps 1-4 under [Generate a DOI](https://projectpythia.org/cookbook-guide.html#generate-a-doi) in the Cookbook Guide. Return here for instructions on step 5, and your final step:
- [ ] **Release your Cookbook!**
    - On the right-hand sidebar for your Cookbook repository, click “Create a new release”. If you don’t see this button, you may need to click on the “Releases” header first and “Create” or “Draft” a new release.
    ![GitHub Repository sidebar section titled "Releases"](https://raw.githubusercontent.com/ProjectPythia/projectpythia.github.io/main/portal/_static/images/4-releases.png "Releases")
    - “Choose a tag”, enter a new tag name. This will be the git reference of the snapshot of code that represents this particular release of your Cookbook! We recommend using a name fitting the [CalVer](https://calver.org/) scheme, so something like v2024.06.13 for the date of the release, then choose “+ Create new tag: <your tag name> on publish” and make its Target main (unless you have the knowledge and desire to release from another branch!)
    ![Interface for generating a new tag on release](https://raw.githubusercontent.com/ProjectPythia/projectpythia.github.io/main/portal/_static/images/5-release-new-tag.png "Create a tag")
    - From here you can use GitHub’s nifty “Generate release notes” button to automatically draft a summary of your Cookbook release based on merged Pull Requests! Feel free to further modify the title and body text of your release notes to fit your Cookbook and best represent your authors.
    - Finally, `Publish release`!
```
