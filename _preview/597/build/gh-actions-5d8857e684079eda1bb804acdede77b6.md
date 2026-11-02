---
title: "When a GitHub Shadowban Breaks Open Source Infrastructure"
subtitle: Overhauling our GitHub Actions to Reduce Compute Minutes and Ghost Commits
date: 2026-05-20
author: jukent
description: What I learned after discovering my GitHub account had been shadowbanned, and how it broke our link checks.
tags: ["github", "actions"]
---

Early April, I discovered that my GitHub account was shadowbanned.

First, I only noticed that links to pull requests I had opened were failing our link checker. But the issue was much larger.

From my side, everything looked normal, but my coworkers were unable to see or interact with my account. I reached out to GitHub for support and was told that they would not be “removing the restrictions from this account.” All of a sudden, this small issue seemed insurmountable.

The closest explanation I received referenced GitHub’s Additional Product Terms for Actions:

> “Any repositories that use GitHub Actions solely to interact with 3rd party websites, to engage in incentivized activities, or for general computing purposes may fall afoul of the GitHub Additional Product Terms.”

I have not used GitHub Actions for cryptomining, unauthorized access, commercial activity, or unrelated computing tasks. Everything I configured was in service of open-source scientific infrastructure through Project Pythia and National Center for Atmospheric Research.

I found and posted on forums and help requests, learning:
1) It is GitHub's policy to not inform anyone of their account being banned and
2) This problem is so common that r/github has a 2 year old [stickied "shadowbanned for no reason?" thread](https://www.reddit.com/r/github/comments/1er6iwo/was_your_account_suspended_deleted_or/) (and you will be banned from that community too if you ask for support out of that thread),
3) There is a [GitHub community discussion page for banned accounts](https://github.com/orgs/community/discussions/136618), where, ironically, you can only see comments from accounts that have had the ban lifted.

I reached out to my community and found someone who knew someone at GitHub who said they would look into the problem for me. But **without explanation, notification, or fanfare, two weeks later my account was back.**

I still do not know for sure what specific behavior triggered this restriction, but I have some theories.

## The Impact

This affects more than just my account. Since the restriction:

1. I cannot review team member pull requests,
2. I cannot merge team member pull requests,
3. I cannot request a review on a pull request,
4. Pull requests I’ve opened have disappeared (even merged ones that should belong to the project),
5. I cannot contribute to conversations on issues,
6. Issues I opened have disappeared,
7. team member’s contributions as comments on issues I’ve opened have disappeared,
8. Links in our project are failing as we may point to a specific merged pull request that has disappeared or to my GitHub account page,
10. There are major impacts on iteration prioritization and planning (not knowing if/when I will be able to contribute, and also issues assigned to/created by/commented on by me do not have accurate status information if they appear at all),
11. I am no longer listed as a contributor in any open source project,
12. I cannot record onboarding videos that leverage GitHub for the upcoming Pythia hackathon,
13. My GitHub account is linked to authorization for certain cloud services (JetStream2 for the Pythia hackathon) which I no longer have access to,
14. The project is potentially using GitHub actions in a way that has too high of a burden and without insight, any other team member’s are at risk of repeating the behavior that flagged my account,
15. Any websites I'm hosting for personal projects are down,
16. My portfolio is essentially up in flames.

Some of these consequences are unexpected; specifically, the idea that merged pull requests associated with my account are not owned by the ProjectPythia GitHub organization, making team members unable to look at commits to main authored by me.

For open-source scientific projects, this becomes an infrastructure problem. This and the lack of communication is particularly devastating, because **how can we teach GitHub best practices if we are unknowingly violating them.**

## The Possible Cause

From what I can gather there are three main theories why a GitHub account can be targeted: Copilot usage, Actions minutes usage, and too many commits.

### 1. Copilot Usage

There seems to have been a mass shadowbanning of GitHub accounts due to copilot usage. My connection at GitHub suggested that this was the likely culprit.

But that seems unlikely to me, with my literally minimal usage:

![0 Copilot Minutes](../../_static/images/posts/gh-actions/copilot-minutes.png)

### 2. Actions minutes

For years, we have used Actions to:

* Build and test JupyterBook-based educational cookbooks
* Run nightly builds
* Deploy documentation sites

One possible clue: we received warnings in March that the organization had used 90% of its included GitHub Actions minutes. We assumed builds would simply stop after the quota reset.

Recently, we migrated to JupyterBook 2, which may have increased build volume or workload. I personally migrated a lot of our 90+ repositories, making me the last person to have touched the actions files within.

Turns out, it is by design that the author of the workflow run is the last author of a workflow file:
* [GitHub Actions terms](https://docs.github.com/en/site-policy/github-terms/github-terms-for-additional-products-and-features?utm_source=chatgpt.com#actions)
* [Scheduled workflow actor behavior](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows?utm_source=chatgpt.com#actor-for-scheduled-workflows)

If this type of automation is being interpreted as “general computing purposes,” many educational and scientific projects may be at risk without realizing it.

Taking a closer look at our GH-Actions usage, we have **twice as many action minutes as there are real minutes** in the month of March. Definitely too much! With the biggest culprit being the Radar Cookbook, and that being triggered by me.

![Tons of Actions Minutes](../../_static/images/posts/gh-actions/action-minutes.png)

To fix this:
1. We immediately (temporarily) shut off all Actions in our organization. You may have noticed pull requests not running their tests.
2. We implemented action time outs for our build and link checks.


### 3. Too many commits

One workflow pattern now seems especially concerning: nightly rebuilds that repeatedly commit updates to `gh-pages`, often attributed to an individual maintainer account (i.e. mine).

I noticed since we changed our Actions in 2025 that I had commits on days I knew I did not work (weekends, holidays, etc).

![Weekend Commits](../../_static/images/posts/gh-actions/weekend-commits.png)

![Weekend Commits 2](../../_static/images/posts/gh-actions/weekend-commits2.png)


I accepted this as a non-issue, in part because it went on for a whole year before the shadowban. And partially because, when I would go to investigate the commits there would be none.

![No Commits](../../_static/images/posts/gh-actions/no-commits.png)

I didn't realize that the previous view defaulted to `main` instead of the branch where the commits are on - `gh-pages`. When I adjust my view, the commits become visible again.

![GH-pages Commits](../../_static/images/posts/gh-actions/gh-pages-commits.png)

And they do look, admittedly, very spammy; pushing Jupyter notebook metadata that does not need to be published.

![Noisy Commits](../../_static/images/posts/gh-actions/noisy-commits.png)

[We exorcised these ghost commits by dropping `gh-pages`](https://github.com/ProjectPythia/cookbook-actions/pull/179) and using the native GitHub-actions bot (instead of a user's account).

Addressing our potential GitHub violations is high enough priority that we accepted that this has the consequence of losing our `gh-pages` based Pull Request previews. Re-instating that functionality is our next priority.

## In Conclusion

More than anything, I want clarity.

* Which repositories or workflows triggered concern?
* What specific behavior violated policy?
* How can maintainers avoid repeating it?

We teach GitHub best practices to the scientific software community. Without clearer guidance, it is difficult for open-source infrastructure projects to know how to operate safely and sustainably on GitHub.

Hopefully, this post can help others know where to look to diagnose a similar issue and reinstate their accounts and serve as transparent documentation of why we made the decisions to change our Actions workflows.
