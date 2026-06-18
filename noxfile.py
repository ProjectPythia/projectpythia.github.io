import nox

# `nox -s docs` / `nox -s docs-live` build and serve the portal site. nox makes
# its own venv with mystmd, so contributors don't create or activate one first.
# (The conda environment.yml is only needed for the analytics scripts.)
nox.options.reuse_existing_virtualenvs = True


@nox.session
def docs(session):
    """Build the portal site once."""
    session.install("mystmd")
    session.chdir("portal")
    session.run("myst", "build", "--html")


@nox.session(name="docs-live")
def docs_live(session):
    """Serve the portal site with live reload at localhost:3000."""
    session.install("mystmd")
    session.chdir("portal")
    session.run("myst", "start")
